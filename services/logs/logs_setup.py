"""Модуль предназначен для реализации формирования логгера для других модулей."""
import logging
import os

from .settings import BASE_FORMAT, BASE_DIR_FOR_LOGGING, BASE_LOG_LEVEL


def get_logger(logger_name: str) -> logging.Logger:
    """
    Функция формирует логгер для заданного пространства имен.

    Args:
        logger_name (str): название пространсва имен, для которого будет создан логгер.

    Returns:
        None
    """
    log_path = os.path.join(BASE_DIR_FOR_LOGGING, f'{logger_name}.log')

    logger = logging.getLogger(logger_name)
    logger.setLevel(BASE_LOG_LEVEL)
    logger_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    logger_formatter = logging.Formatter(BASE_FORMAT)
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    return logger
