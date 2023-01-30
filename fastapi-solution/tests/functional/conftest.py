import asyncio

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
