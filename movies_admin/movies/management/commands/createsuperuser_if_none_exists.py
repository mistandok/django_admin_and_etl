"""Модуль содержит команду для создания суперпользователя."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    Класс предназначен для реализации команды manage.py по созданию суперпользователя, если он отсутствует.

    Пример: manage.py createsuperuser_if_none_exists --user=admin --password=changeme.
    """

    def add_arguments(self, parser):
        """
        Метод добавляет аргументы к команде.

        Args:
            parser: парсер.
        """
        parser.add_argument('--user', required=True)
        parser.add_argument('--password', required=True)
        parser.add_argument('--email', default='admin@example.com')

    def handle(self, *args, **options):
        """
        Метод создает суперпользователя, если такого не существует.

        Args:
            args: позиционные аргументы.
            options: именнованные аргументы.
        """
        user = get_user_model()

        if user.objects.exists():
            return

        username = options['user']
        password = options['password']
        email = options['email']

        user.objects.create_superuser(username=username, password=password, email=email)

        self.stdout.write(f'Local user "{username}" was created')
