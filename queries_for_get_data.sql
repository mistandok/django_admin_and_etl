SET SEARCH_PATH = content, public;


SELECT
    fw.id,
    fw.rating imdb_rating,
    array_agg(DISTINCT g.name) as genre,
    fw.title,
    fw.description,
    array_agg(DISTINCT p.full_name) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'director') director,
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
    fw.modified modified_state
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.modified > '2022-12-25'::DATE
GROUP BY fw.id, fw.modified
ORDER BY fw.modified
LIMIT 100;



WITH person_ids AS (
    SELECT
        p.id
    FROM
        content.person p
    WHERE
        p.modified > '2022-12-25'::DATE
    ORDER BY
        p.modified
)
, film_ids AS (
    SELECT
        fw.id
    FROM
        content.film_work fw
    LEFT JOIN
        content.person_film_work pfw ON fw.id = pfw.film_work_id
    WHERE
        pfw.person_id IN (SELECT p.id from person_ids p)
)
SELECT
    fw.id,
    fw.title,
    fw.description,
    fw.rating,
    fw.type,
    fw.created,
    fw.modified,
    COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
    ) as persons,
    array_agg(DISTINCT g.name) as genres,
    max(p.modified) as modified_state
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.id IN (TABLE film_ids)
GROUP BY fw.id, fw.modified
ORDER BY max(p.modified);


WITH genre_ids AS (
    SELECT
        g.id
    FROM
        content.genre g
    WHERE
        g.modified > '2022-12-25'::DATE
    ORDER BY
        g.modified
    LIMIT 100
)
, film_ids AS (
    SELECT
        fw.id
    FROM
        content.film_work fw
    LEFT JOIN
        content.genre_film_work gfw ON gfw.film_work_id = fw.id
    WHERE
        gfw.genre_id IN (TABLE genre_ids)
    LIMIT 100
)
SELECT
    fw.id,
    fw.title,
    fw.description,
    fw.rating,
    fw.type,
    fw.created,
    fw.modified,
    COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
    ) as persons,
    array_agg(DISTINCT g.name) as genres,
    max(g.modified) as modified_state
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.id IN (TABLE film_ids)
GROUP BY fw.id, fw.modified
ORDER BY max(g.modified);