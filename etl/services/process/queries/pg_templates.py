"""Модуль содержит шаблоны SQL запросов для PostgreSQL."""

MOVIE_BASE_QUERY = """
    {cte}
    SELECT
        fw.id,
        fw.rating imdb_rating,
        array_agg(DISTINCT g.name) FILTER (WHERE g.id IS NOT NULL) as genre,
        fw.title,
        fw.description,
        COALESCE (
            array_agg(DISTINCT p.full_name) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'director'),
            ARRAY[]::text[]
        ) director,
        array_agg(DISTINCT p.full_name) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'actor') actors_names,
        array_agg(DISTINCT p.full_name) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'writer') writers_names,
        COALESCE (
           json_agg(
               DISTINCT jsonb_build_object(
                   'id', p.id,
                   'name', p.full_name
               )
           ) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'actor'),
           '[]'
        ) as actors,
        COALESCE (
           json_agg(
               DISTINCT jsonb_build_object(
                   'id', p.id,
                   'name', p.full_name
               )
           ) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'writer'),
           '[]'
        ) as writers,
        {modified_state_field}
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    {where_condition}
    GROUP BY fw.id, fw.modified
    {order_by}
"""
