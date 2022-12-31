"""Модуль отвечает за тесты validators."""

import unittest

from ..validators.validators import ElasticsearchValidator


class Testing(unittest.TestCase):
    """Класс для тестирования хранилища Редис."""

    def test_all_data_valid(self):
        """Метод проверяет, что все значения валидны."""
        validator = ElasticsearchValidator()
        data_for_validate = [
            {
                'id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3dd',
                'imdb_rating': 4.0,
                'genre': ['Family', 'Game-Show-NEW', 'Music New', 'Reality-TV'],
                'title': 'Star Academy',
                'description': '',
                'director': [],
                'actors_names': ['Nikos Aliagas'],
                'writers_names': None,
                'actors': [{'id': '5a78f3a6-5471-42c2-a5ef-8f45ee9ced63', 'name': 'Nikos Aliagas'}],
                'writers': [],
                '_id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3dd',
            },
            {
                'id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3df',
                'imdb_rating': 9.0,
                'genre': None,
                'title': None,
                'description': None,
                'director': [],
                'actors_names': None,
                'writers_names': None,
                'actors': None,
                'writers': None,
                '_id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3dd',
            },
        ]
        validated_data = list(validator.get_valid_data(data_for_validate))
        self.assertEqual(data_for_validate, validated_data)

    def test_one_row_valid(self):
        """Метод тестирует одну валидную и две невалидные записи."""
        validator = ElasticsearchValidator()
        data_for_validate = [
            {
                'id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3dd',
                'imdb_rating': 4.0,
                'genre': ['Family', 'Game-Show-NEW', 'Music New', 'Reality-TV'],
                'title': 'Star Academy',
                'description': '',
                'director': [],
                'actors_names': ['Nikos Aliagas'],
                'writers_names': None,
                'actors': [{'id': '5a78f3a6-5471-42c2-a5ef-8f45ee9ced63', 'name': 'Nikos Aliagas'}],
                'writers': [],
                '_id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3dd',
            },
            {
                'imdb_rating': 9.0,
                'genre': None,
                'title': None,
                'description': None,
                'director': None,
                'actors_names': None,
                'writers_names': None,
                'actors': None,
                'writers': None,
            },
            {
                'id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3df',
                'imdb_rating': 9.0,
                'genre': 1234,
                'title': 12313,
                'description': 41515555,
                'director': 141414,
                'actors_names': 12414,
                'writers_names': 1414,
                'actors': 142,
                'writers': 41241,
                '_id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3dd',
            },
        ]

        validated_data = list(validator.get_valid_data(data_for_validate))
        self.assertEqual(data_for_validate[:-2], validated_data)

    def test_empty_director(self):
        """Метод теситрует то, что данные с пустым директором не валидны."""
        validator = ElasticsearchValidator()
        data_for_validate = [
            {
                'id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3dd',
                'imdb_rating': 4.0,
                'genre': ['Family', 'Game-Show-NEW', 'Music New', 'Reality-TV'],
                'title': 'Star Academy',
                'description': '',
                'director': None,
                'actors_names': ['Nikos Aliagas'],
                'writers_names': None,
                'actors': [{'id': '5a78f3a6-5471-42c2-a5ef-8f45ee9ced63', 'name': 'Nikos Aliagas'}],
                'writers': [],
                '_id': 'ffaec4b6-477d-4247-add0-dbe2ad91b3dd',
            },
        ]
        validated_data = list(validator.get_valid_data(data_for_validate))
        self.assertEqual([], validated_data)


if __name__ == '__main__':
    unittest.main()
