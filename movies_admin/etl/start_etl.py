"""Модуль отвечает за старт ETL процесса."""

from storages.api import get_backoff_key_value_storage
from config.settings import STATE_STORAGE_PARAMS

if __name__ == '__main__':
    state_storage = get_backoff_key_value_storage(STATE_STORAGE_PARAMS)
