"""Модуль содержит настройки для работы ETL."""
import os
from collections import namedtuple
from pathlib import Path
from enum import Enum

from dotenv import load_dotenv, find_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

BASE_DIR = Path(__file__).resolve().parent.parent

StateStorageAdapterParams = namedtuple('StateStorageAdapterParams', ['storage_type', 'adapter_params'])

EsIndexInfo = namedtuple('EsIndexInfo', ['name', 'file_path'])

load_dotenv(find_dotenv(os.path.join(
    BASE_DIR,
    'config',
    '.env.prod',
)))


class ETLProcessType(str, Enum):
    """Тип доступных ETL процессов."""

    MOVIE_FILM_WORK = 'movie_film_work'
    MOVIE_GENRE = 'movie_genre'
    MOVIE_PERSON = 'movie_person'


class QueryType(str, Enum):
    """Клас описывает доступные типы запросов."""

    PG_MOVIE_FILM_WORK = 'postgres_movie_filmwork'
    PG_MOVIE_GENRE = 'postgres_movie_genre'
    PG_MOVIE_PERSON = 'postgres_movie_person'


class ElasticsearchIndex(Enum):
    """Класс описывает индексы для работы с Elasticsearch."""

    MOVIES = EsIndexInfo('movies', os.path.join(BASE_DIR, 'config', 'es_movies_index.json'))
    GENRES = EsIndexInfo('genres', os.path.join(BASE_DIR, 'config', 'es_genres_index.json'))
    PERSONS = EsIndexInfo('persons', os.path.join(BASE_DIR, 'config', 'es_persons_index.json'))


TIME_TO_RESTART_PROCESSES_SECONDS = 10

REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')

PG_DSL = {
    'dbname': os.environ.get('PG_DB_NAME'),
    'user': os.environ.get('PG_DB_USER'),
    'password': os.environ.get('PG_DB_PASSWORD'),
    'host': os.environ.get('PG_DB_HOST'),
    'port': os.environ.get('PG_DB_PORT'),
}

ES_HOST = os.environ.get('ES_HOST')

ES_PORT = os.environ.get('ES_PORT')

ES_INDEX_JSON_PATH = os.path.join(BASE_DIR, 'config', 'es_movies_index.json')

ES_CONNECTION = f'http://{ES_HOST}:{ES_PORT}'

PROCESS_IS_STARTED_STATE = 'process_is_started'

MODIFIED_STATE = {
    ETLProcessType.MOVIE_FILM_WORK: 'modified_film_work',
    ETLProcessType.MOVIE_GENRE: 'modified_film_work_genre',
    ETLProcessType.MOVIE_PERSON: 'modified_film_work_person',
}

QUERY_TYPE = {
    ETLProcessType.MOVIE_FILM_WORK: QueryType.PG_MOVIE_FILM_WORK,
    ETLProcessType.MOVIE_GENRE: QueryType.PG_MOVIE_GENRE,
    ETLProcessType.MOVIE_PERSON: QueryType.PG_MOVIE_PERSON,
}

PROCESS_ES_INDEX = {
    ETLProcessType.MOVIE_FILM_WORK: ElasticsearchIndex.MOVIES,
    ETLProcessType.MOVIE_GENRE: ElasticsearchIndex.MOVIES,
    ETLProcessType.MOVIE_PERSON: ElasticsearchIndex.MOVIES,
}

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

DB_BUFFER_SIZE = int(os.environ.get('DB_BUFFER_SIZE', 100))
