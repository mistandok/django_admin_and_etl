"""Модуль отвечает за описание Загрузчиков данных в целевую базу."""

from abc import ABC, abstractmethod
from typing import Iterable

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from config.settings import ES_TARGET_INDEX
from services.logs.logs_setup import get_logger

logger = get_logger()


class BaseLoader(ABC):
    """Базовый класс, отвечающий за загрузку данных в целевой объект."""

    @abstractmethod
    def load(self, data_for_load: Iterable) -> bool:
        """
        Метод позволяет загружать данные из в целевой объект.

        Args:
            data_for_load: данные для загрузки.

        Returns:
            True - загрузка прошла успешно, False - загрузка завершилась с ошибками.
        """
        pass


class ElasticsearchLoader(BaseLoader):
    """Класс, отвечающий за загрузку данных в Elasticsearch."""

    def __init__(self, client: Elasticsearch):
        """
        Инициализирующий метод.

        Args:
            client: клиент Elasticsearch.
        """
        self._client = client

    def load(self, data_for_load: Iterable[dict]) -> bool:
        """
        Метод позволяет загружать данные из в целевой объект.

        Args:
            data_for_load: данные для загрузки.

        Returns:
            True - загрузка прошла успешно, False - загрузка завершилась с ошибками.
        """
        logger.info('Загружаем данные в Elasticsearch.')
        bulk(self._client, data_for_load, index=ES_TARGET_INDEX)
        logger.info('Загрузили данные в Elasticsearch.')
        return True
