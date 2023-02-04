import json

import pytest
from elasticsearch import AsyncElasticsearch

from functional.settings import test_settings
from functional.testdata.es_data import genres_data, movies_data, persons_data


@pytest.fixture(scope="session", autouse=True)
async def es_client():
    """
    Create ElasticSearch client and delete all indices after tests
    """
    client = AsyncElasticsearch(test_settings.es_url)
    yield client

    await client.indices.delete(index='movies')
    await client.indices.delete(index='persons')
    await client.indices.delete(index='genres')

    await client.close()


def get_es_bulk_query(
    data: list[dict],
    index: str,
    id_field: str
) -> list[str]:
    """
    Create bulk query for ElasticSearch
    """
    query = []
    for item in data:
        query.extend([
            json.dumps({'index': {'_index': index, '_id': item[id_field]}}),
            json.dumps(item)
        ])
    return query


@pytest.fixture(scope="session")
def es_write_data(es_client):
    """
    Write data to ElasticSearch
    """
    async def inner(data, index):
        if not await es_client.indices.exists(index):
            index_dict = dict(
                test_settings.es_index_mappings[index],
                **test_settings.es_index_settings
            )
            await es_client.indices.create(index, body=index_dict)

        bulk_query = get_es_bulk_query(data, index, test_settings.es_id_field)
        str_query = '\n'.join(bulk_query) + '\n'

        response = await es_client.bulk(str_query, refresh=True)

        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture(scope="session", autouse=True)
async def es_write_films(es_write_data):
    """
    Write films data to ElasticSearch
    """
    await es_write_data(movies_data, 'movies')


@pytest.fixture(scope="session", autouse=True)
async def es_write_persons(es_write_data):
    """
    Write persons data to ElasticSearch
    """
    await es_write_data(persons_data, 'persons')


@pytest.fixture(scope="session", autouse=True)
async def es_write_genres(es_write_data):
    """
    Write genres data to ElasticSearch
    """
    await es_write_data(genres_data, 'genres')
