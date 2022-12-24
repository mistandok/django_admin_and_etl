"""Настройки Django-проекта."""

from dotenv import load_dotenv, find_dotenv
from split_settings.tools import include

load_dotenv(find_dotenv('.env.prod'))

include(
    'components/application_definition.py',
    'components/password_validation.py',
    'components/database.py',
    'components/internationalization.py',
    'components/corsheaders_setup.py',
)
