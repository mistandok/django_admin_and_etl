"""Модуль содержит описание моделей pydantic."""
from functools import lru_cache
from typing import List, Optional

from pydantic import BaseModel
from config.settings import ETLProcessType
from services.logs.logs_setup import get_logger

logger = get_logger()


class PersonMovie(BaseModel):
    """Модель, описывающая персону для фильмов."""

    id: str
    name: str


class GenreMovie(BaseModel):
    """Модель, описывающая жанры для фильмов."""

    id: str
    name: str


class Movie(BaseModel):
    """Модель, описывающая фильм."""

    _id: str
    id: str
    imdb_rating: Optional[float]
    genres: Optional[List[GenreMovie]]
    title: Optional[str]
    description: Optional[str]
    persons: Optional[List[str]]
    directors_names: Optional[List[str]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    actors: Optional[List[PersonMovie]]
    writers: Optional[List[PersonMovie]]
    directors: Optional[List[PersonMovie]]


class Genre(BaseModel):
    """Модель, описывающая жанр."""

    _id: str
    id: str
    name: str
    description: Optional[str]


class Person(BaseModel):
    """Модель, описывающая персону."""

    _id: str
    id: str
    full_name: str
    actor: List[str]
    writer: List[str]
    director: List[str]
    other: List[str]
    films: List[str]


@lru_cache()
def get_model_for_process_type(process_type: ETLProcessType) -> BaseModel:
    """
    Функция определяет модель данных, которая соответствует процессц ETL.

    Args:
        process_type: тип процесса ETL.

    Returns:
        модель данных
    """
    model_map = {
        ETLProcessType.MOVIE_FILM_WORK: Movie,
        ETLProcessType.MOVIE_PERSON: Movie,
        ETLProcessType.MOVIE_GENRE: Movie,
        ETLProcessType.GENRE_CREATED_LINK: Genre,
        ETLProcessType.PERSON_CREATED_LINK: Person,
        ETLProcessType.GENRE_MODIFIED: Genre,
        ETLProcessType.PERSON_MODIFIED: Person,
    }

    try:
        return model_map[process_type]
    except KeyError as error:
        logger.error(f'Для процесса {process_type} не удалось получить модель для валидации данных.')
        raise error
