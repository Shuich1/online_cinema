import logging

from helpers.models import *
from helpers.state_check import JsonFileStorage, State
from psycopg2.extensions import connection as _connection


class DataExtractor:
    def __init__(self, connection: _connection):
        self.connection = connection
        self.state = State(JsonFileStorage())
        self.model_mapping = {'fw': FilmWork,
                              'g': Genre,
                              'p': Person}
        self.index_mapping = {'movies': 'fw',
                              'genres': 'g',
                              'persons': 'p'}
        self.query_mapping = {
            'g':
                """
                SELECT
                    g.id,
                    g.name,
                    g.updated_at
                FROM content.genre g
                {where_clause}
                ORDER BY g.updated_at
                LIMIT {batch_size};
                """,
            'p':
                """
                SELECT
                    p.id,
                    p.full_name,
                    array_agg(DISTINCT pfw.role) as role,
                    array_agg(DISTINCT pfw.film_work_id) as film_ids,
                    p.updated_at
                FROM content.person p
                LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
                {where_clause}
                GROUP BY p.id
                ORDER BY p.updated_at
                LIMIT {batch_size};
                """,
            'fw':
                """
                SELECT
                    fw.id,
                    fw.title,
                    fw.description,
                    fw.rating,
                    fw.type,
                    fw.created_at,
                    fw.updated_at,
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
                    COALESCE (
                        json_agg(
                        DISTINCT jsonb_build_object(
                            'genre_id', g.id,
                            'genre_name', g.name
                        )
                    ) FILTER (WHERE g.id is not null),
                    '[]'
                    ) as genres
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                {where_clause}
                GROUP BY fw.id
                ORDER BY fw.updated_at
                LIMIT {batch_size};
                """}

    def get_data(self, batch_size: int, index_name) -> list:
        cursor = self.connection.cursor()
        table_name = self.index_mapping[index_name]
        load_handler = self.model_mapping[table_name]
        last_state = self.state.get_state('etl_last_modified_{}'.format(table_name))
        if not last_state:
            where_clause = 'WHERE TRUE'
        else:
            where_clause = 'WHERE {table}.updated_at > \'{time}\''.format(table=table_name,
                                                                          time=last_state)
        query = self.query_mapping[table_name].format(where_clause=where_clause, batch_size=batch_size)
        cursor.execute(query)
        data = [load_handler(*d) for d in cursor.fetchall()]
        if not data:
            self.state.set_state('etl_last_modified_{}'.format(table_name), last_state)
            cursor.close()
            return []
        else:
            self.state.set_state('etl_last_modified_{}'.format(table_name), data[-1].updated_at)
            logging.info('Extracted {len} rows, last state {state}'.format(len=len(data),
                                                                           state=data[-1].updated_at))
            cursor.close()
            return data
