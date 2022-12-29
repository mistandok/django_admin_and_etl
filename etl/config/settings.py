"""Модуль содержит настройки для работы ETL."""
import os
from collections import namedtuple
from pathlib import Path
from enum import Enum

from dotenv import load_dotenv, find_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

BASE_DIR = Path(__file__).resolve().parent.parent

StateStorageAdapterParams = namedtuple('StateStorageAdapterParams', ['storage_type', 'adapter_params'])

load_dotenv(find_dotenv(os.path.join(
    BASE_DIR,
    'config',
    '.env.prod',
)))


class ETLProcessType(str, Enum):
    """Тип доступных ETL процессов."""

    FILM_WORK = 'film_work'
    GENRE = 'genre'
    PERSON = 'person'


STATE_STORAGE_TYPE = os.getenv('STATE_STORAGE_TYPE')

REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')


STATE_STORAGE_PARAMS_MAP = {
    'redis': StateStorageAdapterParams(
        storage_type=STATE_STORAGE_TYPE,
        adapter_params={
            'host': REDIS_HOST,
            'port': REDIS_PORT,
        },
    ),
}

STATE_STORAGE_PARAMS = STATE_STORAGE_PARAMS_MAP.get(
    STATE_STORAGE_TYPE,
    StateStorageAdapterParams(storage_type=None, adapter_params=None),
)


PG_DSL = {
    'dbname': os.environ.get('PG_DB_NAME'),
    'user': os.environ.get('PG_DB_USER'),
    'password': os.environ.get('PG_DB_PASSWORD'),
    'host': os.environ.get('PG_DB_HOST'),
    'port': os.environ.get('PF_DB_PORT'),
}


PROCESS_IS_STARTED_STATE = 'process_is_started'


MODIFIED_STATE = {
    ETLProcessType.FILM_WORK: 'modified_film_work',
    ETLProcessType.GENRE: 'modified_genre',
    ETLProcessType.PERSON: 'modified_person',
}

QUERY_TYPE = {
    ETLProcessType.FILM_WORK: 'postgres_filmwork',
    ETLProcessType.GENRE: 'postgres_genre',
    ETLProcessType.PERSON: 'postgres_person',
}
