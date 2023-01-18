import sqlite3
from contextlib import contextmanager
import os
import psycopg2
from psycopg2.extras import DictCursor
from load_data import SQLiteLoader
from upload_data import PGUploader
from dotenv import load_dotenv

load_dotenv()


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


if __name__ == '__main__':
    dsl = {'dbname': os.environ.get('POSTGRES_DB'),
           'user': os.environ.get('POSTGRES_USER'),
           'password': os.environ.get('POSTGRES_PASSWORD'),
           'host': os.environ.get('POSTGRES_HOST'),
           'port': os.environ.get('POSTGRES_PORT')}
    tables = ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work']
    with conn_context(os.environ.get('SQLITE_DB_FILE')) as sqlite_conn,\
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        sqlite_loader = SQLiteLoader(sqlite_conn)
        pg_uploader = PGUploader(pg_conn)
        batch_size = int(os.environ.get('BATCH_SIZE'))

        for table in tables:
            for data in sqlite_loader.load_from_sqlite(table, batch_size):
                pg_uploader.upload_to_pg(table, data)
