"""Модуль отвечает за описание классов и функций для извлечения данных из источника."""

from abc import ABC, abstractmethod
from typing import Any


class BaseExtractor(ABC):
    """Базовый класс, отвечающий за выгрузку данных."""

    @abstractmethod
    def extract(self) -> Any:
        """
        Метод позволяет извлекать данные из объекта источника.

        Returns:
            Возвращает данные из источника.
        """
        pass
