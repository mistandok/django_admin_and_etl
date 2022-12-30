"""Модуль содержит функции, которые создают контекстные менеджеры для подключений к различным источникам."""
from contextlib import contextmanager

from elasticsearch import Elasticsearch
from redis import Redis

from ..decorators.resiliency import backoff


@contextmanager
@backoff()
def redis_context(host: str, port: str) -> Redis:
    """
    Контектсный менеджер для открытия и закрытия подключения к Redis.

    Args:
        host (str): хост.
        port (str): порт.

    Yields:
        соединение с БД.
    """
    client = Redis(host=host, port=port)
    yield client
    client.close()


@contextmanager
@backoff()
def es_context(host: str) -> Elasticsearch:
    """
    Контектсный менеджер для открытия и закрытия подключения к Elasticsearch.

    Args:
        host (str): хост и порт подключения.

    Yields:
        соединение с БД.
    """
    client = Elasticsearch(hosts=[host])
    yield client
    client.close()
