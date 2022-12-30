"""Модуль предназначен для реализации формирования логгера для других модулей."""
import logging
from functools import lru_cache
from logging.handlers import RotatingFileHandler

from .settings import BASE_FORMAT, BASE_LOG_LEVEL, BASE_PATH_FOR_LOG_FILE, BASE_LOGGER_NAME, BASE_LOG_FILE_BYTE_SIZE, \
    BASE_BACKUP_COUNT


@lru_cache()
def get_logger() -> logging.Logger:
    """
    Функция формирует логгер для заданного пространства имен.

    Returns:
        None
    """
    logger = logging.getLogger(BASE_LOGGER_NAME)
    logger.setLevel(BASE_LOG_LEVEL)
    logger_handler = RotatingFileHandler(
        BASE_PATH_FOR_LOG_FILE,
        encoding='utf-8',
        maxBytes=BASE_LOG_FILE_BYTE_SIZE,
        backupCount=BASE_BACKUP_COUNT,
    )
    logger_formatter = logging.Formatter(BASE_FORMAT)
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    return logger
