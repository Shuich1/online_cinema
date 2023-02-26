from http import HTTPStatus

import pytest

from functional.testdata.users_data import test_user


pytestmark = pytest.mark.asyncio


@pytest.mark.order(after='test_register.py::test_register_user')
async def test_logout(make_request):
    response = await make_request(
        'POST',
        '/auth/signin',
        payload=test_user.dict()
    )

    access_token = response['headers']['Authorization']

    response = await make_request(
        'GET',
        '/auth/logout',
        headers={
            'Authorization': access_token
        }
    )

    assert response['status'] == HTTPStatus.OK

    # Trying to get access to resourse with revoked token

    response = await make_request(
        'GET',
        '/auth/history',
        headers={
            'Authorization': access_token
        }
    )

    assert response['status'] == HTTPStatus.UNAUTHORIZED
