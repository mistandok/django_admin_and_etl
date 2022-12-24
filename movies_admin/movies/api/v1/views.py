"""Модуль содержит все views для работы api v1."""
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F
from django.db.models import QuerySet
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesApiMixin:
    """Миксин для представлений, работающих с моделью фильмов."""

    def get_queryset(self) -> QuerySet:
        """Метод возвращает QuerySet.

        Returns:
            QuerySet.
        """
        array_agg_person = (
            lambda person_type:
            ArrayAgg(F('persons__full_name'), filter=Q(personfilmwork__role=person_type), distinct=True)
        )

        return (
            Filmwork.objects.prefetch_related('genres', 'persons').all().
            values('id', 'title', 'description', 'creation_date', 'rating', 'type').
            annotate(
                genres=ArrayAgg(F('genres__name'), distinct=True),
                actors=array_agg_person('actor'),
                directors=array_agg_person('director'),
                writers=array_agg_person('writer'),
            )
        )

    def render_to_response(self, context, **response_kwargs):
        """
        Метод возвращает JSON-ответ.

        Args:
            context: словарь данных для формирования страницы.
            response_kwargs: именованные аргументы.

        Returns:
            JsonResponse.
        """
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """Представление для списка фильмов."""

    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Метод возвращает словарь данных для формирования страницы.

        Args:
            object_list: список объектов.
            kwargs: именнованые аргументы.

        Returns:
            словарь данных для формирования страницы.
        """
        queryset = self.get_queryset()

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by,
        )

        return {
            'results': list(queryset),
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """Представление для конкретного фильма."""

    def get_context_data(self, *args, **kwargs):
        """
        Метод возвращает словарь данных для формирования страницы.

        Args:
            args: позиционные аргументы.
            kwargs: именнованые аргументы.

        Returns:
            словарь данных для формирования страницы.
        """
        return self.object
