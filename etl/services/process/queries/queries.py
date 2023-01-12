"""Модуль отвечает за описание запросов для ETL-процесса."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from config.settings import ETLProcessType, QueryType, MODIFIED_STATE
from services.storages.key_value_storages import KeyValueStorage
from services.logs.logs_setup import get_logger
from .pg_templates import (
    MOVIE_BASE_QUERY, GENRE_CREATED_LINK_QUERY, PERSON_CREATED_LINK_QUERY,
    GENRE_MODIFIED_QUERY, PERSON_MODIFIED_QUERY,
)

logger = get_logger()


class BaseETLQuery(ABC):
    """Базовый класс, для генерации запросов для ETL-процесса."""

    def __init__(self, process_type: ETLProcessType, state_storage: KeyValueStorage):
        """
        Инициализирующий метод.

        Args:
            process_type: Тип ETL-процесса
            state_storage: хранилище состояний для определения modified_state
        """
        self._process_type = process_type
        self._state_storage = state_storage
        self._modified_state_name = MODIFIED_STATE.get(self._process_type)

    @abstractmethod
    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """

    def _get_modified_state(self) -> Optional[datetime]:
        """
        Метод возвращает временное значение из хранилища для modified_state.

        Returns:
            modified_state: текущее значение moified_state в хранилище.
        """
        modified_state = self._state_storage.get_value(self._modified_state_name)
        logger.info(f'modified state для {self._process_type} равно: {modified_state}')
        return modified_state


class MoviePostgreETLQuery(BaseETLQuery):
    """Класс для генерации запросов к PostgreSQL."""

    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """
        logger.info(f'Генерируем запрос для {self._process_type}')
        query = MOVIE_BASE_QUERY.format(
            cte=self._get_cte(),
            modified_state_field=self._get_modified_state_field(),
            where_condition=self._get_where_condition(),
            order_by=self._get_order_by(),
        )
        logger.info(f'Запрос к БД: \n {query}')

        return query

    def _get_cte(self) -> str:
        """
        Метод возвращает SQL для cte, который нужно выполнить для получения данных.

        Returns:
            cte для sql-запроса.
        """
        return ''

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        return ''

    def _get_order_by(self) -> str:
        """
        Метод возвращает order by условия для запроса.

        Returns:
            order by для sql-запроса.
        """
        return ''

    def _get_modified_state_field(self) -> str:
        """
        Метод возвращает order by условия для запроса.

        Returns:
            order by для sql-запроса.
        """
        return 'fw.modified modified_state'


class FilmworkMoviePostgreETLQuery(MoviePostgreETLQuery):
    """Класс помогает сгенерировать запрос для Filmwork."""

    def _get_order_by(self) -> str:
        """
        Метод возвращает order by условия для запроса.

        Returns:
            order by для sql-запроса.
        """
        return 'ORDER BY fw.modified'

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        modified_state = self._get_modified_state()

        if modified_state is None:
            return 'WHERE TRUE'

        return "WHERE fw.modified > '{modified_state}'::timestamp".format(
            modified_state=self._get_modified_state(),
        )


class PersonMoviePostgreETLQuery(MoviePostgreETLQuery):
    """Класс помогает сгенерировать запрос для Person."""

    def _get_cte(self) -> str:
        """
        Метод возвращает SQL для cte, который нужно выполнить для получения данных.

        Returns:
            cte для sql-запроса.
        """
        cte = """
        WITH person_ids AS (
            SELECT
                p.id
            FROM
                content.person p
            {where_condition}
            ORDER BY
                p.modified
        )
        , film_ids AS (
            SELECT
                fw.id
            FROM
                content.film_work fw
            LEFT JOIN
                content.person_film_work pfw ON fw.id = pfw.film_work_id
            WHERE
                pfw.person_id IN (SELECT p.id from person_ids p)
        )
        """
        modified_state = self._get_modified_state()

        if modified_state is None:
            where_condition = 'WHERE TRUE'
        else:
            where_condition = f"WHERE p.modified > '{modified_state}'::timestamp"

        return cte.format(where_condition=where_condition)

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        return 'WHERE fw.id IN (TABLE film_ids)'

    def _get_order_by(self) -> str:
        """
        Метод возвращает order by условия для запроса.

        Returns:
            order by для sql-запроса.
        """
        return 'ORDER BY max(p.modified)'

    def _get_modified_state_field(self) -> str:
        """
        Метод возвращает order by условия для запроса.

        Returns:
            order by для sql-запроса.
        """
        return 'max(p.modified) as modified_state'


class GenreMoviePostgreETLQuery(MoviePostgreETLQuery):
    """Класс помогает сгенерировать запрос для Genre."""

    def _get_cte(self) -> str:
        """
        Метод возвращает SQL для cte, который нужно выполнить для получения данных.

        Returns:
            cte для sql-запроса.
        """
        cte = """
        WITH genre_ids AS (
            SELECT
                g.id
            FROM
                content.genre g
            {where_condition}
            ORDER BY
                g.modified
        )
        , film_ids AS (
            SELECT
                fw.id
            FROM
                content.film_work fw
            LEFT JOIN
                content.genre_film_work gfw ON gfw.film_work_id = fw.id
            WHERE
                gfw.genre_id IN (TABLE genre_ids)
        )
        """
        modified_state = self._get_modified_state()

        if modified_state is None:
            where_condition = 'WHERE TRUE'
        else:
            where_condition = f"WHERE g.modified > '{modified_state}'::timestamp"

        return cte.format(where_condition=where_condition)

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        return 'WHERE fw.id IN (TABLE film_ids)'

    def _get_order_by(self) -> str:
        """
        Метод возвращает order by условия для запроса.

        Returns:
            order by для sql-запроса.
        """
        return 'ORDER BY max(g.modified)'

    def _get_modified_state_field(self) -> str:
        """
        Метод возвращает order by условия для запроса.

        Returns:
            order by для sql-запроса.
        """
        return 'max(g.modified) as modified_state'


class GenreCreatedLinkPostgreETLQuery(BaseETLQuery):
    """
    Класс для генерации запросов к PostgreSQL.

    Формирует запрос для поиска жанров, для которых появилась связь в таблице genre_film_work
    """

    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """
        logger.info(f'Генерируем запрос для {self._process_type}')
        query = GENRE_CREATED_LINK_QUERY.format(
            where_condition=self._get_where_condition(),
        )
        logger.info(f'Запрос к БД: \n {query}')

        return query

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        modified_state = self._get_modified_state()

        if modified_state is None:
            return 'WHERE TRUE'

        return "WHERE gfw.created > '{modified_state}'::timestamp".format(
            modified_state=modified_state,
        )


class PersonCreatedLinkPostgreETLQuery(BaseETLQuery):
    """
    Класс для генерации запросов к PostgreSQL.

    Формирует запрос для поиска персоналий, для которых появилась связь в таблице person_film_work
    """

    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """
        logger.info(f'Генерируем запрос для {self._process_type}')
        query = PERSON_CREATED_LINK_QUERY.format(
            where_condition=self._get_where_condition(),
        )
        logger.info(f'Запрос к БД: \n {query}')

        return query

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        modified_state = self._get_modified_state()

        if modified_state is None:
            return 'WHERE TRUE'

        return "WHERE pfw.created > '{modified_state}'::timestamp".format(
            modified_state=modified_state,
        )


class GenreModifiedPostgreETLQuery(BaseETLQuery):
    """
    Класс для генерации запросов к PostgreSQL.

    Формирует запрос для поиска жанров, для которых существуют фильмы и которые были изменены.
    """

    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """
        logger.info(f'Генерируем запрос для {self._process_type}')
        query = GENRE_MODIFIED_QUERY.format(
            where_condition=self._get_where_condition(),
        )
        logger.info(f'Запрос к БД: \n {query}')

        return query

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        modified_state = self._get_modified_state()

        if modified_state is None:
            return 'WHERE TRUE'

        return "WHERE g.modified > '{modified_state}'::timestamp".format(
            modified_state=modified_state,
        )


class PersonModifiedPostgreETLQuery(BaseETLQuery):
    """
    Класс для генерации запросов к PostgreSQL.

    Формирует запрос для поиска персоналий, для которых появилась связь в таблице person_film_work
    """

    def get_sql(self) -> str:
        """
        Метод возвращает SQL, который нужно выполнить для получения данных.

        Returns:
            sql-запрос.
        """
        logger.info(f'Генерируем запрос для {self._process_type}')
        query = PERSON_MODIFIED_QUERY.format(
            where_condition=self._get_where_condition(),
        )
        logger.info(f'Запрос к БД: \n {query}')

        return query

    def _get_where_condition(self) -> str:
        """
        Метод возвращает where условия для запроса.

        Returns:
            where для sql-запроса.
        """
        modified_state = self._get_modified_state()

        if modified_state is None:
            return 'WHERE TRUE'

        return "WHERE p.modified > '{modified_state}'::timestamp".format(
            modified_state=modified_state,
        )


class ETLQueryFactory:
    """Фабрика классов для ETLQuery."""

    queries = {
        QueryType.PG_MOVIE_FILM_WORK: FilmworkMoviePostgreETLQuery,
        QueryType.PG_MOVIE_PERSON: PersonMoviePostgreETLQuery,
        QueryType.PG_MOVIE_GENRE: GenreMoviePostgreETLQuery,
        QueryType.PG_GENRE_CREATED_LINK: GenreCreatedLinkPostgreETLQuery,
        QueryType.PG_PERSON_CREATED_LINK: PersonCreatedLinkPostgreETLQuery,
        QueryType.PG_GENRE_MODIFIED: GenreModifiedPostgreETLQuery,
        QueryType.PG_PERSON_MODIFIED: PersonModifiedPostgreETLQuery,
    }

    @staticmethod
    def query_by_type(query_type: QueryType, *args, **kwargs) -> BaseETLQuery:
        """
        Метод возвращает инстанс запроса по заданному типу.

        Args:
            query_type: тип ETL процесса.
            args: позиционные аргументы.
            kwargs: именнованные аргументы.

        Returns:
            query (BaseETLQuery): запрос.
        """
        try:
            query_class = ETLQueryFactory.queries[query_type]
            return query_class(*args, **kwargs)
        except KeyError as error:
            logger.error(f'Для типа {query_type} не существует реализации запроса.', exc_info=True)
            raise error
