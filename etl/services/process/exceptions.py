"""Модуль содержит исключения."""


class AnotherProcessIsStartedError(Exception):
    """Класс-исключение. Райзится тогда, когда уже есть запущенные процессы."""

    def __init__(self, process_type: str):
        """
        Инициализирующий метод.

        Args:
            process_type: тип процесса.
        """
        self.process_type = process_type
        self.message = f'Невозможно запустить процесс {process_type}, так как другой процесс находится на выполнении.'
        super().__init__(self.message)
