import sqlite3
from models import *


class SQLiteLoader:
    def __init__(self, connector: sqlite3.Connection):
        self.cursor = connector.cursor()
        self.table_mapping = {'film_work': FilmWork,
                              'genre': Genre,
                              'person': Person,
                              'genre_film_work': GenreFilmWork,
                              'person_film_work': PersonFilmWork}

    def load_from_sqlite(self, table_name: str, batch_size: int):
        load_handler = self.table_mapping[table_name]
        try:
            offset = 0
            query = 'SELECT * FROM {name} ORDER BY id LIMIT {batch_size} '.format(name=table_name,
                                                                                  batch_size=batch_size)
            self.cursor.execute(query+'OFFSET {batch_offset};'.format(batch_offset=batch_size * offset))
            data = [load_handler(**dict(d)) for d in self.cursor.fetchmany(batch_size)]

            while data:
                yield data
                offset += 1
                self.cursor.execute(query+'OFFSET {batch_offset};'.format(batch_offset=batch_size * offset))
                data = [load_handler(**dict(d)) for d in self.cursor.fetchmany(batch_size)]
        except sqlite3.Error as error:
            print('Failed to read data from table {}'.format(error))
