"""Модуль содержит настройки для работы ETL."""
import os
from collections import namedtuple
from dataclasses import dataclass
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


@dataclass(frozen=True)
class EsIndexInfo:
    """Класс описывает информацию об индексе эластики."""

    name: str
    file_path: str


class ETLProcessType(str, Enum):
    """Тип доступных ETL процессов."""

    MOVIE_FILM_WORK = 'movie_film_work'
    MOVIE_GENRE = 'movie_genre'
    MOVIE_PERSON = 'movie_person'
    GENRE_CREATED_LINK = 'genre_created_link'
    PERSON_CREATED_LINK = 'person_created_link'
    GENRE_MODIFIED = 'genre_modified'
    PERSON_MODIFIED = 'person_modified'


class QueryType(str, Enum):
    """Клас описывает доступные типы запросов."""

    PG_MOVIE_FILM_WORK = 'pg_movie_filmwork'
    PG_MOVIE_GENRE = 'pg_movie_genre'
    PG_MOVIE_PERSON = 'pg_movie_person'
    PG_GENRE_CREATED_LINK = 'pg_genre_created_link'
    PG_PERSON_CREATED_LINK = 'pg_person_created_link'
    PG_PERSON_MODIFIED = 'pg_person_modified'
    PG_GENRE_MODIFIED = 'pg_genre_modified'


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

ES_CONNECTION = f'http://{ES_HOST}:{ES_PORT}'

PROCESS_IS_STARTED_STATE = 'process_is_started'

MODIFIED_STATE = {
    ETLProcessType.MOVIE_FILM_WORK: 'modified_film_work',
    ETLProcessType.MOVIE_GENRE: 'modified_film_work_genre',
    ETLProcessType.MOVIE_PERSON: 'modified_film_work_person',
    ETLProcessType.PERSON_CREATED_LINK: 'modified_person_created_link',
    ETLProcessType.GENRE_CREATED_LINK: 'modified_genre_created_link',
    ETLProcessType.PERSON_MODIFIED: 'modified_person',
    ETLProcessType.GENRE_MODIFIED: 'modified_genre',
}

QUERY_TYPE = {
    ETLProcessType.MOVIE_FILM_WORK: QueryType.PG_MOVIE_FILM_WORK,
    ETLProcessType.MOVIE_GENRE: QueryType.PG_MOVIE_GENRE,
    ETLProcessType.MOVIE_PERSON: QueryType.PG_MOVIE_PERSON,
    ETLProcessType.PERSON_CREATED_LINK: QueryType.PG_PERSON_CREATED_LINK,
    ETLProcessType.GENRE_CREATED_LINK: QueryType.PG_GENRE_CREATED_LINK,
    ETLProcessType.PERSON_MODIFIED: QueryType.PG_PERSON_MODIFIED,
    ETLProcessType.GENRE_MODIFIED: QueryType.PG_GENRE_MODIFIED,
}

PROCESS_ES_INDEX = {
    ETLProcessType.MOVIE_FILM_WORK: ElasticsearchIndex.MOVIES,
    ETLProcessType.MOVIE_GENRE: ElasticsearchIndex.MOVIES,
    ETLProcessType.MOVIE_PERSON: ElasticsearchIndex.MOVIES,
    ETLProcessType.GENRE_CREATED_LINK: ElasticsearchIndex.GENRES,
    ETLProcessType.PERSON_CREATED_LINK: ElasticsearchIndex.PERSONS,
    ETLProcessType.PERSON_MODIFIED: ElasticsearchIndex.PERSONS,
    ETLProcessType.GENRE_MODIFIED: ElasticsearchIndex.GENRES,
}

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

DB_BUFFER_SIZE = int(os.environ.get('DB_BUFFER_SIZE', 100))
