"""Модуль отвечает за описание хранилищ типа Key-Value."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional

from redis import Redis
from .storage_typing import RedisKey, RedisValue

from ..logs.logs_setup import get_logger

logger = get_logger()


class StorageType(str, Enum):
    """Клас описывает доступные типы Key-Value хранилищ."""

    REDIS = 'redis'


class KeyValueStorage(ABC):
    """Базовый класс-интерфейс для хранилищ типа Key-Value."""

    @abstractmethod
    def get_value(self, key: Any) -> Optional[Any]:
        """
        Метод извлекает значение для указанного ключа из хранилища.

        Args:
            key (Any): ключ для поиска значения.

        Returns:
            value (Any): значение для указанного ключа
        """

    @abstractmethod
    def set_value(self, key: Any, key_value: Any):
        """
        Метод устанавливает значение для указанного ключа.

        Args:
            key (Any): ключ для поиска значения.
            key_value (Any): значение для указанного ключа
        """

    @abstractmethod
    def delete_keys(self, *keys: Any):
        """
        Метод удаляет ключ из хранилища.

        Args:
            keys (Any): ключ для удаления.
        """


class RedisStorage(KeyValueStorage):
    """Класс для работы с хранилищем Redis."""

    def __init__(self, redis_adapter: Redis):
        """
        Инициализирующий метод.

        Args:
            redis_adapter (Redis): адаптер, который позволяет работать с реализацией хранилища.
        """
        self.redis_adater = redis_adapter

    def get_value(self, key: RedisKey) -> Optional[RedisValue]:
        """
        Метод извлекает значение для указанного ключа из хранилища.

        Args:
            key (RedisKey): ключ для поиска значения.

        Returns:
            value (RedisValue): значение для указанного ключа
        """
        key_value = self.redis_adater.get(key)
        return self.decode_value(key_value)

    def set_value(self, key: RedisKey, key_value: RedisValue):
        """
        Метод устанавливает значение для указанного ключа.

        Args:
            key (RedisKey): ключ для поиска значения.
            key_value (RedisValue): значение для указанного ключа
        """
        self.redis_adater.set(key, key_value)

    def delete_keys(self, *keys: Any):
        """
        Метод удаляет ключ из хранилища.

        Args:
            keys (Any): ключ для удаления.
        """
        self.redis_adater.delete(*keys)

    @staticmethod
    def decode_value(value_for_decode: bytes) -> Optional[RedisValue]:
        """
        Функция декодирует значения.

        Args:
            value_for_decode (bytes): значение для декодирования.

        Returns:
            decoded_value (Optional[RedisValue]): декодированное значение.
        """
        try:
            return value_for_decode.decode('utf-8')
        except UnicodeDecodeError as error:
            logger.error(f'Не удалось декодировать значение {value_for_decode}', exc_info=True)
            raise error
        except AttributeError:
            return None


class KeyValueStorageFactory:
    """Фабрика классов для Key-Value хранилищ."""

    storages = {
        StorageType.REDIS: RedisStorage,
    }

    @staticmethod
    def storage_by_type(storage_type: StorageType, *args, **kwargs) -> KeyValueStorage:
        """
        Метод возвращает инстанс хранилища по заданному типу.

        Args:
            storage_type: тип хранилища.
            args: позиционные аргументы.
            kwargs: именнованные аргументы.

        Returns:
            starage (KeyValueStorage): хранилище.
        """
        try:
            storage_class = KeyValueStorageFactory.storages[storage_type]
            return storage_class(*args, **kwargs)
        except KeyError as error:
            logger.error(f'Для хранилища типа {storage_type.value} не существует реализации.', exc_info=True)
            raise error


class StorageAdapterFactory:
    """Фабрика классов для адаптеров хранилищ."""

    storage_adapters = {
        StorageType.REDIS: Redis,
    }

    @staticmethod
    def storage_adapter_by_type(storage_type: StorageType, *args, **kwargs) -> Any:
        """
        Метод возвращает инстанс адаптера хранилища по заданному типу.

        Args:
            storage_type: тип хранилища.
            args: позиционные аргументы.
            kwargs: именнованные аргументы.

        Returns:
            starage_adapter (Any): адаптер хранилища.
        """
        try:
            storage_adapter = StorageAdapterFactory.storage_adapters[storage_type]
            return storage_adapter(*args, **kwargs)
        except KeyError as error:
            logger.error(f'Для хранилища типа {storage_type.value} не существует адаптера хранилища.', exc_info=True)
            raise error
