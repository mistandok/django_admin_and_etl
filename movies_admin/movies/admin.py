"""Модуль администирования моделями."""

from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для Жанр."""


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Админка для Человек."""


class GenreFilmworkInline(admin.TabularInline):
    """Встроенная админка для жанров кинопроизведения."""

    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    """Встроенная админка для людей кинопроизведения."""

    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Админка для Человек."""

    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )

    list_display = ('title', 'type', 'creation_date', 'rating')

    list_filter = ('type',)

    search_fields = ('title', 'description', 'id')
