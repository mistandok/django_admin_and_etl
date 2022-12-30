"""Модуль отвечает за адаптирование данных, получаемых с помощь Извлекателей данных к требуемому формату."""


from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generator, Optional

from .extractors import BaseExtractor


class Row(dict):
    """Класс-помощник для адаптируемых строк."""

    def exclude_fields(self, *field_names: str):
        """
        Метод удаляет поля из объекта.

        Args:
            field_names (str): наименование поля.
        """
        for field_name in field_names:
            if field_name not in self.keys():
                continue
            self.pop(field_name)


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

        fields_for_exclude = ['modified_state']

        for row in extracted:
            row = Row(row)
            row.exclude_fields(*fields_for_exclude)
            row.update({'_id': row.get('id')})
            yield row
