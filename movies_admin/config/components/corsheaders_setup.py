"""Модуль отвечает за настройки, относящиеся к corsheaders."""

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    'http://localhost:8080',
]
