"""Модуль содержит классы и функции, помогающие задавать параметры для ETL-процессов."""
import json

from http import HTTPStatus
from psycopg2.extensions import connection as postgre_conn
from redis import Redis
from elasticsearch import Elasticsearch
from config.settings import QUERY_TYPE, DB_BUFFER_SIZE, PROCESS_ES_INDEX, EsIndexInfo
from services.logs.logs_setup import get_logger
from services.process.extractors.adapters import PostgreToElasticsearchAdapter
from services.process.extractors.extractors import PostgreExtractor
from services.process.processes import ETLProcessType, ETLProcessParameters
from services.process.queries.queries import ETLQueryFactory
from services.process.loaders.loaders import ElasticsearchLoader
from services.process.validators.validators import ElasticsearchValidator
from services.process.validators.pydantic_models import get_model_for_process_type
from services.storages.key_value_storages import RedisStorage
from services.storages.key_value_decorators import BackoffKeyValueDecorator

logger = get_logger()


def get_index_info_by_process(process_type: ETLProcessType) -> EsIndexInfo:
    """
    Функция возвращает информация об индексе для конкретного процесса.

    Args:
        process_type: тип процесса.

    Returns:
        EsIndexInfo
    """
    try:
        return PROCESS_ES_INDEX[process_type].value
    except KeyError as error:
        logger.error(f'Для процесса {process_type} не задан индекс в Elasticsearch')
        raise error


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
    index_info = get_index_info_by_process(etl_process_type)
    state_storage = BackoffKeyValueDecorator(RedisStorage(redis_client))
    query = ETLQueryFactory.query_by_type(
        query_type=QUERY_TYPE.get(etl_process_type),
        process_type=etl_process_type,
        state_storage=state_storage,
    )
    extractor = PostgreToElasticsearchAdapter(PostgreExtractor(pg_conn, query, DB_BUFFER_SIZE))
    validator = ElasticsearchValidator(get_model_for_process_type(etl_process_type))
    loader = ElasticsearchLoader(es_client, index_info.name, validator)

    return ETLProcessParameters(
        state_storage=state_storage,
        process_type=etl_process_type,
        extractor=extractor,
        loader=loader,
    )


def drop_es_index(es_client: Elasticsearch, *indexes: str):
    """
    Вспомогательная функция для обнуления состояний и удаления данных из es.

    Args:
        es_client: клиент эластики
        indexes: наименование индекса, который нужно удалить.
    """
    for index in indexes:
        es_client.options(
            ignore_status=[HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND],
        ).indices.delete(index=index)


def create_es_index_if_not_exists(es_client: Elasticsearch, *indexes_info: EsIndexInfo):
    """
    Вспомогательная функция, которая создает индекс в Elasticsearch, если его там нет.

    Args:
        es_client: клиент Elasticsearch.
        indexes_info: наименование индекса, который нужно создать.
    """
    for index_info in indexes_info:
        if not es_client.indices.exists(index=index_info.name):
            with open(index_info.file_path, 'r') as index_settings_file:
                index_settings = json.load(index_settings_file)
                es_client.indices.create(index=index_info.name, ignore=HTTPStatus.BAD_REQUEST, body=index_settings)
