"""Модуль отвечает за старт ETL процесса."""
import contextlib
from time import sleep

import psycopg2
from psycopg2.extras import DictCursor
from config.settings import (
    PG_DSL, ES_CONNECTION, REDIS_HOST, REDIS_PORT, ETLProcessType, TIME_TO_RESTART_PROCESSES_SECONDS,
)
from services.decorators.resiliency import backoff
from services.context_managers.managers import redis_context, es_context
from services.process.helpers import get_etl_params_for_redis_pg_es
from services.process.processes import ETLProcess
from services.process.helpers import create_es_index_if_not_exists


def main():
    """Основная функция, стартующая ETL-процессы."""
    connect = backoff()(psycopg2.connect)

    with redis_context(REDIS_HOST, REDIS_PORT) as redis, es_context(ES_CONNECTION) as es, \
            contextlib.closing(connect(**PG_DSL, cursor_factory=DictCursor)) as pg:
        create_es_index_if_not_exists(es)
        while True:
            for process_type in ETLProcessType:
                etl_params = get_etl_params_for_redis_pg_es(process_type, pg, redis, es)
                with ETLProcess(etl_params) as process:
                    process.start()
            sleep(TIME_TO_RESTART_PROCESSES_SECONDS)


if __name__ == '__main__':
    main()
