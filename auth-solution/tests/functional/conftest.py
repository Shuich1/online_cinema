from random import randint

import aiohttp
import pytest

from .settings import test_settings
from .testdata.users_data import superuser, test_user


pytestmark = pytest.mark.asyncio


@pytest.fixture
def make_request():
    """
    Fixture for making requests to the auth service
    """
    async def inner(
        method: str,
        url: str,
        payload: dict = None,
        params: dict = None,
        headers: dict = None
    ):
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                test_settings.service_url + url,
                json=payload,
                params=params,
                headers=headers | {
                    'X-Request-Id': 'pytest'
                } if headers else {
                    'X-Request-Id': 'pytest'
                }
            ) as response:
                return {
                    'status': response.status,
                    'json': await response.json(),
                    'headers': response.headers
                }
    return inner


@pytest.fixture
async def sign_in(make_request):
    response = await make_request(
        'POST',
        '/auth/signin',
        payload=test_user.dict()
    )

    return {
        'access_token': response['headers']['Authorization'],
        'refresh_token': response['json']['refresh_token']
    }


@pytest.fixture
async def superuser_sign_in(make_request):
    response = await make_request(
        'POST',
        '/auth/signin',
        payload=superuser.dict()
    )

    return {
        'access_token': response['headers']['Authorization'],
        'refresh_token': response['json']['refresh_token']
    }


@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return randint(0, 10000)
