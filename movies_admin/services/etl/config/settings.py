"""Модуль содержит настройки для работы ETL."""
import os
from collections import namedtuple
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

from movies_admin.services.storages.key_value_storages import KyeValueStorageType

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

StateStorageAdapterParams = namedtuple('StateStorageAdapterParams', ['storage_type', 'params'])

load_dotenv(find_dotenv(os.path.join(
    ROOT_DIR,
    'config',
    '.env.prod',
)))

REDIS_PORT = os.getenv('REDIS_PORT')

REDIS_HOST = os.getenv('REDIS_HOST')

STATE_STORAGE = KyeValueStorageType.REDIS

STATE_STORAGE_ADAPTER = StateStorageAdapterParams(
    storage_type=KyeValueStorageType.REDIS,
    params={
        'host': REDIS_HOST,
        'port': REDIS_PORT,
    },
)
