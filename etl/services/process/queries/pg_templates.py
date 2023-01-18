"""Модуль содержит шаблоны SQL запросов для PostgreSQL."""

MOVIE_BASE_QUERY = """
    {cte}
    SELECT
        fw.id,
        fw.rating imdb_rating,
        COALESCE (
           json_agg(
               DISTINCT jsonb_build_object(
                   'id', g.id,
                   'name', g.name
               )
           ) FILTER (WHERE g.id IS NOT NULL),
           '[]'
        ) as genres,
        fw.title,
        fw.description,
        array_agg(DISTINCT p.id::text) FILTER (WHERE p.id IS NOT NULL) persons,
        array_agg(DISTINCT p.full_name) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'director') directors_names,
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
        COALESCE (
           json_agg(
               DISTINCT jsonb_build_object(
                   'id', p.id,
                   'name', p.full_name
               )
           ) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'director'),
           '[]'
        ) as directors,
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

PERSON_CREATED_LINK_QUERY = """
    SELECT DISTINCT
        p.id,
        p.full_name,
        COALESCE(array_agg(DISTINCT pfw.film_work_id::text) FILTER (WHERE pfw.role = 'actor'), ARRAY[]::text[]) actor,
        COALESCE(
            array_agg(DISTINCT pfw.film_work_id::text) FILTER (WHERE pfw.role = 'director'), ARRAY[]::text[]
        ) director,
        COALESCE(array_agg(DISTINCT pfw.film_work_id::text) FILTER (WHERE pfw.role = 'writer'), ARRAY[]::text[]) writer,
        COALESCE(
            array_agg(DISTINCT pfw.film_work_id::text) FILTER (WHERE pfw.role NOT IN ('writer', 'director', 'actor')),
            ARRAY[]::text[]
        ) other,
        COALESCE(array_agg(DISTINCT pfw.film_work_id::text), ARRAY[]::text[]) films,
        pfw.created as modified_state
    FROM
        content.person_film_work pfw
    INNER JOIN
        content.person p
    ON
        p.id = pfw.person_id
    {where_condition}
    GROUP BY p.id, p.full_name, pfw.created
    ORDER BY pfw.created
"""

PERSON_MODIFIED_QUERY = """
    SELECT DISTINCT
        p.id,
        p.full_name,
        COALESCE(array_agg(DISTINCT pfw.film_work_id::text) FILTER (WHERE pfw.role = 'actor'), ARRAY[]::text[]) actor,
        COALESCE(
            array_agg(DISTINCT pfw.film_work_id::text) FILTER (WHERE pfw.role = 'director'), ARRAY[]::text[]
        ) director,
        COALESCE(array_agg(DISTINCT pfw.film_work_id::text) FILTER (WHERE pfw.role = 'writer'), ARRAY[]::text[]) writer,
        p.modified as modified_state
    FROM
        content.person_film_work pfw
    INNER JOIN
        content.person p
    ON
        p.id = pfw.person_id
    {where_condition}
    GROUP BY p.id, p.full_name, p.modified
    ORDER BY p.modified
"""

GENRE_CREATED_LINK_QUERY = """
    SELECT DISTINCT
        g.id,
        g.name,
        g.description,
        gfw.created as modified_state
    FROM
        content.genre_film_work gfw
    INNER JOIN
        content.genre g
    ON
        g.id = gfw.genre_id
    {where_condition}
    ORDER BY gfw.created
"""

GENRE_MODIFIED_QUERY = """
    SELECT DISTINCT
        g.id,
        g.name,
        g.description,
        g.modified as modified_state
    FROM
        content.genre_film_work gfw
    INNER JOIN
        content.genre g
    ON
        g.id = gfw.genre_id
    {where_condition}
    ORDER BY g.modified
"""
