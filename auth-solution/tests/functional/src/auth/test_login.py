from http import HTTPStatus

import pytest

from functional.testdata.users_data import unregistered_email, test_user

pytestmark = pytest.mark.asyncio


@pytest.mark.order(after='test_register.py::test_register_user')
async def test_login(make_request):
    response = await make_request(
        'POST',
        '/auth/signin',
        payload=test_user.dict()
    )

    assert response['status'] == HTTPStatus.OK
    assert response['headers']['Authorization'] is not None
    assert response['json']['refresh_token'] is not None


@pytest.mark.order(after='test_register.py::test_register_user')
async def test_wrong_password_login(make_request, faker):
    response = await make_request(
        'POST',
        '/auth/signin',
        payload={
            'email': test_user.email,
            'password': faker.password()
        }
    )

    assert response['status'] == HTTPStatus.UNAUTHORIZED
    assert 'Authorization' not in response['headers']


async def test_unregistered_user_login(make_request):
    response = await make_request(
        'POST',
        '/auth/signin',
        payload={
            'email': unregistered_email,
            'password': test_user.password
        }
    )

    assert response['status'] == HTTPStatus.UNAUTHORIZED
    assert 'Authorization' not in response['headers']
