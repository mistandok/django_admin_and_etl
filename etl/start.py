"""Модуль отвечает за старт ETL процесса."""
import contextlib

import psycopg2
from psycopg2.extras import DictCursor
from config.settings import STATE_STORAGE_PARAMS, PG_DSL, QUERY_TYPE
from services.storages.api import get_backoff_key_value_storage
from services.process.processes import ETLProcess, ETLProcessType, ETLProcessParameters
from services.process.extractors.extractors import PostgreExtractor
from services.process.queries.queries import ETLQueryFactory
from services.decorators.resiliency import backoff

if __name__ == '__main__':
    backoff_connect = backoff()(psycopg2.connect)
    state_storage = get_backoff_key_value_storage(STATE_STORAGE_PARAMS)
    with contextlib.closing(backoff_connect(**PG_DSL, cursor_factory=DictCursor)) as conn:
        process_type = ETLProcessType.FILM_WORK

        query = ETLQueryFactory.query_by_type(
            QUERY_TYPE.get(process_type),
            process_type=process_type,
            state_storage=state_storage,
        )
        extractor = PostgreExtractor(conn, query)
        etl_params = ETLProcessParameters(
            state_storage=state_storage,
            process_type=process_type,
            loader=None,
            extractor=extractor,
        )
        with ETLProcess(etl_params) as process:
            process.start()
