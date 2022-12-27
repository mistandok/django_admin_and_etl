"""Модуль отвечает за адаптирование данных, получаемых с помощь Извлекателей данных к требуемому формату."""


from abc import ABC, abstractmethod
from typing import Any

from .extractors import BaseExtractor


class BaseExtractorAdapter(ABC):
    """Базовый класс, отвечающий за выгрузку данных."""

    def __init__(self, extractor: BaseExtractor):
        """
        Инициализирующий метод.

        Args:
            extractor: загрузчик, который нужно адаптировать под требуемый формат.
        """
        self._extractor = extractor

    @abstractmethod
    def extract(self) -> Any:
        """
        Метод позволяет извлекать данные из объекта источника, адаптирует их под нужный формат.

        Returns:
            Возвращает адаптированные данные из источника.
        """
        pass
