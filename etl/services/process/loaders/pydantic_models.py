"""Модуль содержит описание моделей pydantic."""
from typing import List, Optional

from pydantic import BaseModel


class Person(BaseModel):
    """Модель, описывающая персону."""

    id: str
    name: str


class Movie(BaseModel):
    """Модель, описывающая фильм."""

    _id: str
    id: str
    imdb_rating: Optional[float]
    genre: Optional[List[str]]
    title: Optional[str]
    description: Optional[str]
    director: Optional[List[str]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    actors: Optional[List[Person]]
    writers: Optional[List[Person]]
