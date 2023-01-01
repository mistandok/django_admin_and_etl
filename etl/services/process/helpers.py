"""Модуль содержит классы и функции, помогающие задавать параметры для ETL-процессов."""
import json

from psycopg2.extensions import connection as postgre_conn
from redis import Redis
from elasticsearch import Elasticsearch
from config.settings import QUERY_TYPE, ES_TARGET_INDEX, ES_INDEX_JSON_PATH, DB_BUFFER_SIZE
from services.process.extractors.adapters import PostgreToElasticsearchAdapter
from services.process.extractors.extractors import PostgreExtractor
from services.process.processes import ETLProcessType, ETLProcessParameters
from services.process.queries.queries import ETLQueryFactory
from services.process.loaders.loaders import ElasticsearchLoader
from services.storages.key_value_storages import RedisStorage
from services.storages.key_value_decorators import BackoffKeyValueDecorator


def get_etl_params_for_redis_pg_es(
    etl_process_type: ETLProcessType,
    pg_conn: postgre_conn,
    redis_client: Redis,
    es_client: Elasticsearch,
) -> ETLProcessParameters:
    """
    Функция возвращает параметры для ETL-процесса.

    В данном случае это выгрузка из PostgreSQL в Elasticsearch, где хранилище состояний - Redis.

    Args:
        etl_process_type: тип ETL-процесса.
        pg_conn: содениение с PostgreSQL.
        redis_client: клиент Redis.
        es_client: клиент Elasticsearch

    Returns:
        ETLProcessParameters
    """
    state_storage = BackoffKeyValueDecorator(RedisStorage(redis_client))
    query = ETLQueryFactory.query_by_type(
        query_type=QUERY_TYPE.get(etl_process_type),
        process_type=etl_process_type,
        state_storage=state_storage,
    )
    extractor = PostgreToElasticsearchAdapter(PostgreExtractor(pg_conn, query, DB_BUFFER_SIZE))
    loader = ElasticsearchLoader(es_client, ES_TARGET_INDEX)

    return ETLProcessParameters(
        state_storage=state_storage,
        process_type=etl_process_type,
        extractor=extractor,
        loader=loader,
    )


def drop_es(es_client: Elasticsearch):
    """
    Вспомогательная функция для обнуления состояний и удаления данных из es.

    Args:
        es_client: клиент эластики
    """
    es_client.options(ignore_status=[400, 404]).indices.delete(index=ES_TARGET_INDEX)


def create_es_index_if_not_exists(es_client: Elasticsearch):
    """
    Вспомогательная функция, которая создает индекс в Elasticsearch, если его там нет.

    Args:
        es_client: клиент Elasticsearch.
    """
    ignore_error = 400

    if not es_client.indices.exists(index=ES_TARGET_INDEX):
        with open(ES_INDEX_JSON_PATH, 'r') as index_settings_file:
            index_settings = json.load(index_settings_file)
            es_client.indices.create(index=ES_TARGET_INDEX, ignore=ignore_error, body=index_settings)
