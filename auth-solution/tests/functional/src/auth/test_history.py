from http import HTTPStatus

import pytest
from functional.testdata.users_data import test_auth_history

pytestmark = pytest.mark.asyncio


@pytest.mark.order(after='test_register.py::test_register_user')
async def test_history(make_request, sign_in):
    access_token = sign_in['access_token']

    response = await make_request(
        'GET',
        '/auth/history/1',
        headers={
            'Authorization': access_token
        }
    )

    assert response['status'] == HTTPStatus.OK
    assert response['json'][-1].keys() == test_auth_history.keys()


@pytest.mark.order(after='test_register.py::test_register_user')
async def test_history_without_auth(make_request):
    response = await make_request(
        'GET',
        '/auth/history/1'
    )

    assert response['status'] == HTTPStatus.UNAUTHORIZED
