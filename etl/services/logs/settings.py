"""Модуль отвечает за настройки для логирования."""
import os
from logging import INFO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

BASE_DIR_FOR_LOGGING = os.path.join(BASE_DIR, 'etl_logs')

BASE_FORMAT = '%(name)s %(asctime)s %(levelname)s %(message)s'

BASE_LOG_LEVEL = INFO