"""Модуль отвечает за старт ETL процесса."""
import contextlib

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection
from config.settings import STATE_STORAGE_PARAMS, PG_DSL, QUERY_TYPE
from services.storages.api import get_backoff_key_value_storage
from services.process.processes import ETLProcess, ETLProcessType, ETLProcessParameters
from services.process.extractors.extractors import PostgreExtractor
from services.process.queries.queries import ETLQueryFactory
from services.decorators.resiliency import backoff


def get_pg_to_es_etl_params(process_type: ETLProcessType, connection: _connection) -> ETLProcessParameters:
    """
    Функция подготавливает параметры для старта ETL-процесса.

    Данные выгружаются из PostgreSQL и загружаются в Elasticsearch.

    Args:
        connection: соединение с базой данных.
        process_type: тип запускаемого процесса.

    Returns:
        параметры для ETL-процесса.
    """
    state_storage = get_backoff_key_value_storage(STATE_STORAGE_PARAMS)
    query = ETLQueryFactory.query_by_type(
        query_type=QUERY_TYPE.get(process_type),
        process_type=process_type,
        state_storage=state_storage,
    )
    extractor = PostgreExtractor(connection, query)
    loader = None

    return ETLProcessParameters(
        state_storage=state_storage,
        process_type=process_type,
        extractor=extractor,
        loader=loader,
    )


def main():
    """Основная функция, стартующая ETL-процессы."""
    connect = backoff()(psycopg2.connect)

    with contextlib.closing(connect(**PG_DSL, cursor_factory=DictCursor)) as conn:
        for process_type in ETLProcessType:
            etl_params = get_pg_to_es_etl_params(process_type, conn)
            with ETLProcess(etl_params) as process:
                process.start()


if __name__ == '__main__':
    main()
