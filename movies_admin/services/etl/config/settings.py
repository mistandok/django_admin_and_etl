"""Модуль содержит настройки для работы ETL."""
import os
from collections import namedtuple
from pathlib import Path
from enum import Enum

from dotenv import load_dotenv, find_dotenv

from movies_admin.services.storages.key_value_storages import KyeValueStorageType

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

StateStorageAdapterParams = namedtuple('StateStorageAdapterParams', ['storage_type', 'adapter_params'])

load_dotenv(find_dotenv(os.path.join(
    ROOT_DIR,
    'config',
    '.env.prod',
)))

REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')

STATE_STORAGE_PARAMS = StateStorageAdapterParams(
    storage_type=KyeValueStorageType.REDIS,
    adapter_params={
        'host': REDIS_HOST,
        'port': REDIS_PORT,
    },
)

PROCESS_IS_STARTED = 'process_is_started'


class ETLProcessType(str, Enum):
    """Тип доступных ETL процессов."""

    FILM_WORK = 'film_work'
    GENRE = 'genre'
    PERSON = 'person'


MODIFIED_STATE = {
    ETLProcessType.FILM_WORK: 'modified_film_work',
    ETLProcessType.GENRE: 'modified_genre',
    ETLProcessType.PERSON: 'modified_person',
}
