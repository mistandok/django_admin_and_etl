"""Модуль отвечает за валидаторы данных, которые мы хотим загрузить."""
from abc import ABC, abstractmethod
from typing import Generator, Iterable

from pydantic import ValidationError, BaseModel
from services.logs.logs_setup import get_logger

logger = get_logger()


class BaseValidator(ABC):
    """Класс отвечает за валидацию данных, которые получает."""

    @abstractmethod
    def get_valid_data(self, data_for_validate: Iterable[dict]) -> Generator:
        """
        Метод предоставляет валидные данные для загрузки из предоставленног списка.

        Args:
            data_for_validate: итерируемый объект для валидации.
        """


class ElasticsearchValidator(BaseValidator):
    """Класс отвечает за валидацию данных для выгрузки в Elasticsearch."""

    def __init__(self, model: BaseModel):
        """
        Инициализирующий метод.

        Args:
            model: модель, по которой валидируют данные.
        """
        self.model = model

    def get_valid_data(self, data_for_validate: Iterable[dict]) -> Generator:
        """
        Метод предоставляет валидные данные для загрузки из предоставленног списка.

        Args:
            data_for_validate: итерируемый объект для валидации.

        Yields:
            генератор валидных данных.
        """
        logger.info('Отбираем только валидные данные.')
        for row in data_for_validate:
            if self._validate_row(row):
                yield row

    def _validate_row(self, row: dict) -> bool:
        """
        Метод проверяет конкретную строку на валидность.

        Args:
            row: строка для проверки.

        Returns:
            True - строка валидна, False - строка не валидна.
        """
        try:
            self.model(**row)
            return True
        except ValidationError:
            logger.warning(f'Запись невалидна: {row}')
            return False
