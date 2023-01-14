from elasticsearch7 import Elasticsearch, helpers, ConnectionTimeout
import logging
import backoff


@backoff.on_exception(backoff.expo, ConnectionTimeout, max_time=60)
def loader(es: Elasticsearch, films: list) -> tuple:
    query = [{'_index': 'movies', '_id': film['id'], '_source': film} for film in films]
    rows_count, errors = helpers.bulk(es, query)
    if errors:
        logging.error('Failed load data to elastic {error}'.format(error=errors))

    return rows_count, errors
