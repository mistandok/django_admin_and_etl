"""Модуль отвечает за описание Загрузчиков данных в целевую базу."""

from abc import ABC, abstractmethod
from typing import Iterable

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from services.logs.logs_setup import get_logger

from ..validators.validators import ElasticsearchValidator

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

    def __init__(self, client: Elasticsearch, target_index: str, validator: ElasticsearchValidator):
        """
        Инициализирующий метод.

        Args:
            client: клиент Elasticsearch.
            target_index: целевой индекс для загрузки.
            validator: валидатор загружаемых данных.
        """
        self._client = client
        self._validator = validator
        self._target_index = target_index

    def load(self, data_for_load: Iterable[dict]) -> bool:
        """
        Метод позволяет загружать данные в целевой объект.

        Args:
            data_for_load: данные для загрузки.

        Returns:
            True - загрузка прошла успешно, False - загрузка завершилась с ошибками.
        """
        logger.info('Загружаем данные в Elasticsearch.')
        valid_data = self._validator.get_valid_data(data_for_load)
        bulk(self._client, valid_data, index=self._target_index)
        logger.info('Загрузили данные в Elasticsearch.')
        return True
