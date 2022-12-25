"""Модуль отвечает за тесты Redis хранилища."""

import unittest
from datetime import datetime

from redis import Redis

from ..key_value_storages import RedisStorage


def get_redis_storage() -> RedisStorage:
    """
    Функция создает RedisStorage.

    Returns:
        redis_storage (RedisStorage): хранилище редис.
    """
    redis_adapter = Redis(port=6379)
    return RedisStorage(redis_adapter)


class Testing(unittest.TestCase):
    """Класс для тестирования хранилища Редис."""

    def test_set_str_value(self):
        """Метод отвечает за тестирование записи str значения в хранилище."""
        storage = get_redis_storage()
        key = 'key'
        key_value = 'my_string_value'

        storage.set_value(key, key_value)
        self.assertEqual(key_value, storage.get_value(key))

    def test_set_int_value(self):
        """Метод отвечает за тестирование записи int значения в хранилище."""
        storage = get_redis_storage()
        key = 'key'
        key_value = 1

        storage.set_value(key, key_value)
        self.assertEqual(key_value, int(storage.get_value(key)))

    def test_set_float_value(self):
        """Метод отвечает за тестирование записи float значения в хранилище."""
        storage = get_redis_storage()
        key = 'key'
        key_value = 12.5

        storage.set_value(key, key_value)
        self.assertEqual(key_value, float(storage.get_value(key)))

    def test_set_datetime_value(self):
        """Метод отвечает за тестирование записи datetime значения в хранилище."""
        storage = get_redis_storage()
        key = 'key'
        current_datetime = datetime.now()
        current_datetime_str = current_datetime.strftime('%d/%m/%Y %H:%M:%S.%f')

        storage.set_value(key, current_datetime_str)
        storage_value_datetime = datetime.strptime(storage.get_value(key), '%d/%m/%Y %H:%M:%S.%f')

        self.assertEqual(current_datetime, storage_value_datetime)

    def test_get_empty_value(self):
        """Метод отвечает за тестирование поиска несуществующего значения в хранилище."""
        storage = get_redis_storage()
        key = 'i_am_mot_exists_in_redis'

        storage_value = storage.get_value(key)

        self.assertEqual(None, storage_value)


if __name__ == '__main__':
    unittest.main()
