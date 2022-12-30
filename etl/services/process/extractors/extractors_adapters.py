"""Модуль отвечает за адаптирование данных, получаемых с помощь Извлекателей данных к требуемому формату."""


from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generator, Optional

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
    def extract(self) -> Generator:
        """
        Метод позволяет извлекать данные из объекта источника, адаптирует их под нужный формат.

        Returns:
            Возвращает адаптированные данные из источника.
        """
        return self._extractor.extract()

    @property
    def last_modified_state(self) -> Optional[datetime]:
        """
        Свойство возвращает последнее modified_state, которое было извлечено с помощью extractor.

        Returns:
            datetime
        """
        return self._extractor.last_modified_state


class PostgreToElasticsearchAdapter(BaseExtractorAdapter):
    """Класс преобразует данные из формата PostgreЫЙД к формату, требуемому в Elasticsearch."""

    def extract(self) -> Generator[dict, None, None]:
        """
        Метод позволяет извлекать данные из объекта источника, адаптирует их под нужный формат.

        Yields:
            Возвращает адаптированные данные из источника.
        """
        extracted = super().extract()

        for row in extracted:
            yield dict(row)
