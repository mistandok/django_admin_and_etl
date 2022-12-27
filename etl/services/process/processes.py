"""Модуль отвечает за основной процесс по выгрузке данных из источника и загрузке данных в целевой объект."""
from dataclasses import dataclass

from config.settings import ETLProcessType, PROCESS_IS_STARTED_STATE
from .extractors import BaseExtractor
from .loaders import BaseLoader
from .extractors_adapters import BaseExtractorAdapter
from .exceptions import AnotherProcessIsStartedError

from ..decorators.resiliency import backoff
from ..storages.key_value_storages import KeyValueStorage
from ..storages.key_value_decorators import BaseKeyValueDecorator
from ..logs.logs_setup import get_logger

logger = get_logger()


@dataclass
class ETLProcessParameters:
    """Класс описывает параметры для ETL-процесса."""

    process_type: ETLProcessType
    state_storage: KeyValueStorage | BaseKeyValueDecorator
    extractor: BaseExtractor | BaseExtractorAdapter
    loader: BaseLoader


class ETLProcess:
    """
    Класс отвечает за процесс перегонки данных из итсточника в целевую систему.

    Настоятельно рекомендуется работать с классом через контекстный менеджер with.
    """

    def __init__(self, etl_params: ETLProcessParameters):
        """
        Инициализирующий метод.

        Включают в себя process_type (Тип процесса, с какоой таблицы тянем данные),
        state_storage (Хранилище состояний, из него берем состояния для процесса),
        extractor (Извлекатель данных, может быть передан обернутым в адаптер, если такой есть. Это нужно
        для того, чтобы подогнать данные под loader),
        loader (Загрузчик данных в целевую систему.).

        Args:
            etl_params: параметры ETL процесса.
        """
        self._process_type = etl_params.process_type
        self._state_storage = etl_params.state_storage
        self._extractor = etl_params.extractor
        self._loader = etl_params.loader

    @backoff()
    def __enter__(self):
        """
        Метод для контекстного менеджера.

        Блокирует работу для других процессов, пока этот процесс не завершится.
        Если есть другие запущенные процессы, то уйдет в ожидание до тех пор, пока другой процесс не завершится.

        Returns:
            ETLProcess
        """
        self.block_process_state()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Метод для контекстного менеджера.

        Разблокирует состояние процесса, чтобы другие процессы могли начать выполнение.

        Args:
            exc_type: стандартная сигнатура запуска контекстного менеджера.
            exc_val: стандартная сигнатура запуска контекстного менеджера.
            exc_tb: стандартная сигнатура запуска контекстного менеджера.
        """
        self.open_process_state()

    def start(self) -> bool:
        """
        Метод стартует процесс по перегонке данных.

        Returns:
            True - процесс завершен успешно, иначе - False.
        """
        try:
            data_for_load = self._extractor.extract()
            self._loader.load(data_for_load)
            return True
        except Exception:
            logger.error(f'Во время выполнения ETL-процесса {self._process_type} произошла непредвиденная ошибка.')
            return False

    def block_process_state(self):
        """
        Метод блокирует выполнение для других процессов в случае, если оно уже не заблокировано.

        Raise:
            AnotherProcessIsStartedError
        """
        if self._is_another_process_started():
            raise AnotherProcessIsStartedError(self._process_type)

        logger.info(f'Процесс {self._process_type} заблокировал работу для других процессов.')
        self._toggle_process(True)

    def open_process_state(self):
        """Разблокирует выполнение для других процессов."""
        logger.info(f'Процесс {self._process_type} завершился. Другие процессы могут начать выполнение.')
        self._toggle_process(False)

    def _is_another_process_started(self) -> bool:
        """
        Метод проверяет, не запущен ли другой процесс.

        Проверка происходит на основе состояния PROCESS_IS_STARTED_STATE.

        Returns:
            True - другие процессы сейчас запущены. False - другие процессы не запущены.
        """
        is_started = self._state_storage.get_value(PROCESS_IS_STARTED_STATE)

        try:
            is_started = bool(int(is_started))
        except (ValueError, TypeError):
            logger.info('Непонятное значение в хранилище состояний. Думаем, что другие процессы не стартавали.')
            is_started = False

        return is_started

    def _toggle_process(self, is_started: bool):
        """
        Метод переключает состояние процесса с помозью хранилища состояний.

        Args:
            is_started: True - процесс запущен, False - процесс завершен.
        """
        self._state_storage.set_value(PROCESS_IS_STARTED_STATE, int(is_started))
