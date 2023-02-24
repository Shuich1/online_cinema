from http import HTTPStatus

import pytest

from functional.testdata.users_data import test_user


pytestmark = pytest.mark.asyncio


async def test_register_user(make_request):
    response = await make_request(
        'POST',
        '/auth/signup',
        payload=test_user.dict()
    )

    assert response['status'] == HTTPStatus.CREATED
    assert response['headers']['Authorization'] is not None
    assert response['json']['refresh_token'] is not None


@pytest.mark.order(after='test_register.py::test_register_user')
async def test_register_existing_user(make_request):
    print(test_user.email)
    response = await make_request(
        'POST',
        '/auth/signup',
        payload=test_user.dict()
    )

    assert response['status'] == HTTPStatus.CONFLICT
