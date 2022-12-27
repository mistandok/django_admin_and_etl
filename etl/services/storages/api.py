"""Модуль содержит api для работы хранилищами."""

from config.settings import StateStorageAdapterParams

from .key_value_storages import StorageAdapterFactory, KeyValueStorageFactory
from .key_value_decorators import BackoffKeyValueDecorator


def get_backoff_key_value_storage(state_storage_params: StateStorageAdapterParams) -> BackoffKeyValueDecorator:
    """
    Функция инициализирует отказоустойчивой key-value хранилище.

    Args:
        state_storage_params: параметры хранилища.

    Returns:
        отказоустойчивое хланилище.
    """
    storage_type = state_storage_params.storage_type
    adapter_params = state_storage_params.adapter_params

    storage_adapter = StorageAdapterFactory.storage_adapter_by_type(storage_type, **adapter_params)
    state_storage = KeyValueStorageFactory.storage_by_type(storage_type, storage_adapter)

    return BackoffKeyValueDecorator(state_storage)
