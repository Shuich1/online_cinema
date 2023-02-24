from random import randint

import aiohttp
import pytest

from .settings import test_settings


@pytest.fixture
def make_get_request():
    """
    Fixture for making GET requests to the auth service
    """
    async def inner(url: str, params: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                test_settings.service_url + url,
                params=params,
                headers = headers
            ) as response:
                return {
                    'status': response.status,
                    'json': await response.json(),
                    'headers': response.headers
                }
    return inner


@pytest.fixture
def make_post_request():
    """
    Fixture for making POST requests to the auth service
    """
    async def inner(url: str, payload: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                test_settings.service_url + url,
                json = payload,
                headers = headers,
            ) as response:
                return {
                    'status': response.status,
                    'json': await response.json(),
                    'headers': response.headers
                }
    return inner


@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return randint(0, 10000)
