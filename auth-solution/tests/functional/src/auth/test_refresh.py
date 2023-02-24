from http import HTTPStatus

import pytest

from functional.testdata.users_data import invalid_refresh_token


@pytest.mark.asyncio
@pytest.mark.order(after='test_register.py::test_register_user')
async def test_refresh(make_request, sign_in):
    refresh_token = sign_in['refresh_token']

    response = await make_request(
        'POST',
        '/auth/refresh_token',
        headers={
            'Authorization': f'Bearer {refresh_token}'
        }
    )

    assert response['status'] == HTTPStatus.OK
    assert response['headers']['Authorization'] is not None


@pytest.mark.asyncio
@pytest.mark.order(after='test_register.py::test_register_user')
async def test_invalid_refresh(make_request):
    response = await make_request(
        'POST',
        '/auth/refresh_token',
        headers={
            'Authorization': f'Bearer {invalid_refresh_token}'
        }
    )

    assert response['status'] == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'Authorization' not in response['headers']


@pytest.mark.asyncio
@pytest.mark.order(after='test_register.py::test_register_user')
async def test_revoked_refresh_token(make_request, sign_in):
    refresh_token = sign_in['refresh_token']

    await make_request(
        'POST',
        '/auth/refresh_token',
        headers={
            'Authorization': f'Bearer {refresh_token}'
        }
    )

    response = await make_request(
        'POST',
        '/auth/refresh_token',
        headers={
            'Authorization': f'Bearer {refresh_token}'
        }
    )

    assert response['status'] == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'Authorization' not in response['headers']
