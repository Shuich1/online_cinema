from dotenv import load_dotenv
import os
import psycopg2
from elasticsearch7 import Elasticsearch
from contextlib import contextmanager
import backoff
from time import sleep
import logging
from psycopg2.extras import DictCursor
from psycopg2 import OperationalError
from extract import DataExtractor
from transform import transformer
from load import loader, movies_index


load_dotenv()


@backoff.on_exception(backoff.expo, OperationalError, max_time=60)
def postgres_conn():
    pg_dsl = {'dbname': os.environ.get('POSTGRES_DB'),
              'user': os.environ.get('POSTGRES_USER'),
              'password': os.environ.get('POSTGRES_PASSWORD'),
              'host': os.environ.get('POSTGRES_HOST'),
              'port': os.environ.get('POSTGRES_PORT')}
    conn = psycopg2.connect(**pg_dsl, cursor_factory=DictCursor)
    return conn


@contextmanager
def postgres_conn_context():
    conn = postgres_conn()
    yield conn
    conn.close()


if __name__ == '__main__':
    batch_size = int(os.environ.get('BATCH_SIZE'))
    while True:
        with postgres_conn_context() as pg_conn:

            extractor = DataExtractor(pg_conn)
            es_client = Elasticsearch(os.environ.get('ES_DOCKER_URL'))
            if not es_client.indices.exists(index="movies"):
                es_client.indices.create(index='movies', body=movies_index)
            while True:
                data = extractor.get_film_data(batch_size)
                if not data:
                    break
                t_data = transformer(data)
                rows_count, errors = loader(es_client, t_data)
            logging.info('All data transferred.')
        sleep(int(os.getenv('TIME_TO_SLEEP')))
