import aiohttp
import pytest

from functional.settings import test_settings


@pytest.fixture
def make_get_request():
    """
    Fixture for making GET requests to the fastapi service
    """
    async def inner(url: str, params: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(test_settings.service_url + '/api/v1' + url, params=params) as response:
                return {
                    'status': response.status,
                    'json': await response.json()
                }
    return inner
