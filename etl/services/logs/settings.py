"""Модуль отвечает за настройки для логирования."""
import os
from logging import INFO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

BASE_DIR_FOR_LOGGING = os.path.join(BASE_DIR, 'etl_logs')

BASE_PATH_FOR_LOG_FILE = os.path.join(BASE_DIR_FOR_LOGGING, 'etl_process_log.log')

BASE_LOGGER_NAME = 'etl_process'

BASE_FORMAT = '%(name)s %(asctime)s %(levelname)s %(message)s'

BASE_LOG_LEVEL = INFO

BASE_LOG_FILE_BYTE_SIZE = 5 * 1024 * 1024

BASE_BACKUP_COUNT = 4
