from http import HTTPStatus

import pytest
from functional.testdata.users_data import test_user_change

pytestmark = pytest.mark.asyncio


@pytest.mark.order(-1)
async def test_change_user(make_request, sign_in):
    access_token = sign_in['access_token']

    response = await make_request(
        'PUT',
        '/auth/change',
        payload=test_user_change.dict(),
        headers={
            'Authorization': access_token
        }
    )

    assert response['status'] == HTTPStatus.OK

    await make_request(
        'GET',
        '/auth/logout',
        headers={
            'Authorization': access_token
        }
    )

    response = await make_request(
        'POST',
        '/auth/signin',
        payload=test_user_change.dict()
    )

    assert response['status'] == HTTPStatus.OK
    assert response['headers']['Authorization'] is not None
    assert response['json']['refresh_token'] is not None
