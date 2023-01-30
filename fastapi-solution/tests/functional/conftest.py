import asyncio
import json

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch

from .settings import test_settings


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def es_client():
    client = AsyncElasticsearch(test_settings.es_url)
    yield client
    await client.close()


@pytest.fixture(scope="session", autouse=True)
async def redis_client():
    client = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
        minsize=10,
        maxsize=20
    )
    yield client
    client.close()

def get_es_bulk_query(data: list[dict], index: str, id_field: str) -> list[str]:
    query = []
    for item in data:
        query.extend([
            json.dumps({'index': {'_index': index, '_id': item[id_field]}}),
            json.dumps(item)
        ])
    return query

@pytest.fixture
def es_write_data(es_client):
    async def inner(data, index):
        bulk_query = get_es_bulk_query(data, index, test_settings.es_id_field)
        str_query = '\n'.join(bulk_query) + '\n'

        response = await es_client.bulk(str_query, refresh=True)

        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner
