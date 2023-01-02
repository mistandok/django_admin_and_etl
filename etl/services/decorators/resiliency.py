"""Модуль отвечает за декораторы, которые помогают обеспечить отказоустойчивость работы функций."""
from functools import wraps
from time import sleep

from ..logs.logs_setup import get_logger

logger = get_logger()


def backoff(start_sleep_time: float = 1, factor: int = 2, border_sleep_time: float = 10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.

    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания
    (border_sleep_time).
    Формулы - t = start_sleep_time * 2^(n) if t < border_sleep_time. t = border_sleep_time if t >= border_sleep_time.

    Args:
        start_sleep_time: начальное время повтора.
        factor: во сколько раз нужно увеличить время ожидания.
        border_sleep_time: граничное время ожидания.

    Returns:
        результат выполнения функции.
    """

    def func_wrapper(func):
        """
        Враппер для функции.

        Args:
            func: функция, которую оборачиваем в декоратор

        Returns:
            callable.
        """
        @wraps(func)
        def inner(*args, **kwargs):
            """
            Сам декоратор. Обеспечивает отказоустойчивость выполнения декорируемой функции.

            Args:
                args: позиционные параметры.
                kwargs: именнованные параметры.

            Returns:
                рузультат функции.
            """
            sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    logger.error(
                        f'Ошибка выполнения функции {func.__name__}. Попытка выполнить снова...',
                        exc_info=True,
                    )
                    if sleep_time < border_sleep_time:
                        sleep_time = start_sleep_time * (2 ^ int(factor))
                    else:
                        sleep_time = border_sleep_time

                    sleep(sleep_time)

        return inner

    return func_wrapper
