"""Модуль отвечает за декораторы к Key-Value хранилищам."""
from abc import ABC
from typing import Any, Optional

from .key_value_storages import KeyValueStorage
from ..decorators.resiliency import backoff


class BaseKeyValueDecorator(ABC):
    """Интерфейс декоратора для работы с Key-Value хранилищем."""

    def __init__(self, storage: KeyValueStorage):
        """
        Инициализирующий метод.

        Args:
            storage: декорируемое хранилище.
        """
        self._storage = storage

    def get_value(self, key: Any) -> Optional[Any]:
        """
        Метод извлекает значение для указанного ключа из хранилища.

        Args:
            key (Any): ключ для поиска значения.

        Returns:
            value (Any): значение для указанного ключа
        """
        return self._storage.get_value(key)

    def set_value(self, key: Any, key_value: Any):
        """
        Метод устанавливает значение для указанного ключа.

        Args:
            key (Any): ключ для поиска значения.
            key_value (Any): значение для указанного ключа
        """
        self._storage.set_value(key, key_value)


class BackoffKeyValueDecorator(BaseKeyValueDecorator):
    """Декоратор для хранилища, обеспечивающий отказоустойчивую работу с хранилищем."""

    @backoff()
    def get_value(self, key: Any) -> Optional[Any]:
        """
        Метод извлекает значение для указанного ключа из хранилища.

        Args:
            key (Any): ключ для поиска значения.

        Returns:
            value (Any): значение для указанного ключа
        """
        return super().get_value(key)

    @backoff()
    def set_value(self, key: Any, key_value: Any):
        """
        Метод устанавливает значение для указанного ключа.

        Args:
            key (Any): ключ для поиска значения.
            key_value (Any): значение для указанного ключа
        """
        super().set_value(key, key_value)
