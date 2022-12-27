"""Модуль предназначен для реализации формирования логгера для других модулей."""
import logging

from .settings import BASE_FORMAT, BASE_LOG_LEVEL, BASE_PATH_FOR_LOG_FILE, BASE_LOGGER_NAME


def get_logger() -> logging.Logger:
    """
    Функция формирует логгер для заданного пространства имен.

    Returns:
        None
    """
    logger = logging.getLogger(BASE_LOGGER_NAME)
    logger.setLevel(BASE_LOG_LEVEL)
    logger_handler = logging.FileHandler(BASE_PATH_FOR_LOG_FILE, mode='w', encoding='utf-8')
    logger_formatter = logging.Formatter(BASE_FORMAT)
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    return logger
