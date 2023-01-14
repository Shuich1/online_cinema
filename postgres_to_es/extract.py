from psycopg2.extensions import connection as _connection
from state_check import State
from state_check import JsonFileStorage
import logging


class DataExtractor:
    def __init__(self, connection: _connection):
        self.connection = connection
        self.state = State(JsonFileStorage())

    def get_film_data(self, batch_size: int) -> list:
        cursor = self.connection.cursor()
        last_state = self.state.get_state('etl_last_modified')
        if not last_state:
            where_clause = 'WHERE TRUE'
        else:
            where_clause = 'WHERE fw.updated_at > \'{time}\''.format(time=last_state)
        film_query = """
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
                    array_agg(DISTINCT g.name) as genres
                    FROM content.film_work fw
                    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                    LEFT JOIN content.person p ON p.id = pfw.person_id
                    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                    LEFT JOIN content.genre g ON g.id = gfw.genre_id
                    {where_clause}
                    GROUP BY fw.id
                    ORDER BY fw.updated_at
                    LIMIT {batch_size};
                """.format(where_clause=where_clause,
                           batch_size=batch_size)
        cursor.execute(film_query)
        film_data = cursor.fetchall()
        if not film_data:
            self.state.set_state('etl_last_modified', last_state)
            cursor.close()
            return []
        else:
            self.state.set_state('etl_last_modified', film_data[-1][6])
            logging.info('Extracted {len} rows'.format(len=len(film_data)))
            cursor.close()
            return film_data
