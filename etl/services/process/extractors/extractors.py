"""Модуль отвечает за описание классов и функций для извлечения данных из источника."""

from abc import ABC, abstractmethod
from typing import Generator
from datetime import datetime

from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictRow

from services.logs.logs_setup import get_logger
from ..queries.queries import PostgreETLQuery

logger = get_logger()


class BaseExtractor(ABC):
    """
    Базовый класс, отвечающий за выгрузку данных.

    Attributes:
        last_modified_state (datetime): последнее modified_state, которое извлекли из генератора extract.
    """

    def __init__(self):
        """Инициализирующий метод."""
        self.last_modified_state: datetime = None

    @abstractmethod
    def extract(self) -> Generator:
        """
        Метод позволяет извлекать данные из объекта источника.

        Returns:
            Возвращает данные из источника.
        """
        pass


class PostgreExtractor(BaseExtractor):
    """Класс для извлечения данных из PostgreSQL."""

    def __init__(self, connection: _connection, query: PostgreETLQuery):
        """
        Инициализаирующий метод.

        Args:
            connection: соединение с PostgreSQL.
            query: Запрос, который необходимо выполнить для извлечения данных.
        """
        super().__init__()
        self._conn = connection
        self._query = query

    def extract(self) -> Generator[DictRow, None, None]:
        """
        Метод позволяет извлекать данные из объекта источника.

        Yields:
            Generator[DictRow, None, None]: генератор данных из объекта.

        Raises:
            psycopg2.Error: ошибка выполнения sql-команды.
        """
        logger.info('Считываем данные из PostgreSQL.')

        with self._conn.cursor() as cursor:
            cursor.execute(self._query.get_sql())

            while True:
                table_data = cursor.fetchmany(100)

                if not table_data:
                    break

                for row in table_data:
                    yield row
                    self.last_modified_state = row.get('modified_state')
