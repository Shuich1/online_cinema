import logging
import os
from contextlib import contextmanager
from time import sleep

import backoff
import psycopg2
from elasticsearch7 import Elasticsearch
from extract import DataExtractor
from load import index_mappings, index_settings, loader
from psycopg2 import OperationalError
from psycopg2.extras import DictCursor
from transform import transformer

logging.basicConfig(level=logging.INFO)


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
    indexes = ['movies', 'genres', 'persons']
    while True:
        with postgres_conn_context() as pg_conn:

            extractor = DataExtractor(pg_conn)
            es_client = Elasticsearch(os.environ.get('ES_DOCKER_URL'))
            # iterating through indexes
            for index in indexes:
                if not es_client.indices.exists(index=index):
                    index_dict = dict(index_mappings[index], **index_settings)
                    es_client.indices.create(index=index, body=index_dict)
                while True:
                    data = extractor.get_data(batch_size, index)
                    if not data:
                        break
                    t_data = transformer(data, index)
                    rows_count, errors = loader(es_client, t_data, index)
            logging.info('All data transferred.')
        sleep(int(os.getenv('TIME_TO_SLEEP')))
