"""Модуль для описания моделей."""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """Абстрактная модель для добавления полей в другие модели."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Абстрактная модель для добавления полей в другие модели."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Описание модели таблицы Жанр."""

    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        indexes = [
            models.Index(fields=['modified'], name='genre_modified_idx'),
        ]

    def __str__(self):
        """
        Строковое представление.

        Returns:
            str: представление в виде строки
        """
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    """Описание модели таблицы Персона."""

    full_name = models.TextField(_('full_name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        indexes = [
            models.Index(fields=['full_name'], name='person_full_name_idx'),
            models.Index(fields=['modified'], name='person_modified_idx'),
        ]

    def __str__(self):
        """
        Строковое представление.

        Returns:
            str: представление в виде строки
        """
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Описание модели таблицы Кинопроизведение."""

    class Type(models.TextChoices):
        MOVIE = 'movie', _('Film')
        TV_SHOW = 'tv_show', _('TV show')

    title = models.CharField(_('title'), blank=False, max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    type = models.CharField(
        _('type'),
        max_length=20,
        choices=Type.choices,
        default=Type.MOVIE,
        blank=False,
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
        indexes = [
            models.Index(fields=['title'], name='film_work_title_idx'),
            models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
            models.Index(fields=['rating'], name='film_work_rating_idx'),
            models.Index(fields=['modified'], name='film_work_modified_idx'),
        ]

    def __str__(self):
        """
        Строковое представление.

        Returns:
            str: представление в виде строки
        """
        return self.title


class GenreFilmwork(UUIDMixin):
    """Описание модели таблицы связей кинопроизведений и жанров."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Filmwork genre')
        verbose_name_plural = _('Filmwork genres')
        unique_together = [
            ['film_work', 'genre'],
        ]
        indexes = [
            models.Index(fields=['created'], name='genre_film_work_created_idx'),
        ]

    def __str__(self):
        """
        Строковое представление.

        Returns:
            str: представление в виде строки
        """
        return _('The film {film} belongs to the genre {genre}').format(
            film=self.film_work.title,
            genre=self.genre.name,
        )


class PersonFilmwork(UUIDMixin):
    """Описание модели таблицы связей кинопроизведений и участников съемочного процесса."""

    class RoleType(models.TextChoices):
        ACTOR = 'actor', _('Actor')
        WRITER = 'writer', _('Writer')
        DIRECTOR = 'director', _('Director')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=RoleType.choices,
        default=RoleType.ACTOR,
        blank=False,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Filmwork participant')
        verbose_name_plural = _('Filmwork participants')
        unique_together = [
            ['film_work', 'person', 'role'],
        ]
        indexes = [
            models.Index(fields=['created'], name='person_film_work_created_idx'),
        ]

    def __str__(self):
        """
        Строковое представление.

        Returns:
            str: представление в виде строки
        """
        return _('{person} participated in the filming of {film}').format(
            film=self.film_work.title,
            person=self.person.full_name,
        )
