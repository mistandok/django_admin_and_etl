"""Модуль отвечает за описание Загрузчиков данных в целевую базу."""

from abc import ABC, abstractmethod
from typing import Any


class BaseLoader(ABC):
    """Базовый класс, отвечающий за загрузку данных в целевой объект."""

    @abstractmethod
    def load(self, data_for_load: Any):
        """
        Метод позволяет загружать данные из в целевой объект.

        Args:
            data_for_load: данные для загрузки.
        """
        pass
