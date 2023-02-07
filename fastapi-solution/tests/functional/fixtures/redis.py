import aioredis
import pytest

from functional.settings import test_settings


@pytest.fixture(scope="session", autouse=True)
async def redis_client():
    """
    Create Redis client and flush all data after tests
    """
    client = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
        minsize=10,
        maxsize=20
    )
    yield client
    client.flushall()
    client.close()
