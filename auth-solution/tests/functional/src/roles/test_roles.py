from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_create_role(make_request, superuser_sign_in):
    access_token = superuser_sign_in['access_token']

    response = await make_request(
        'POST',
        '/roles/role',
        payload=dict(name='reader'),
        headers=dict(Authorization=access_token)
    )
    assert response['status'] == HTTPStatus.OK


async def test_get_roles(make_request, superuser_sign_in):
    access_token = superuser_sign_in['access_token']

    response = await make_request('GET', '/roles', headers=dict(Authorization=access_token))
    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) > 0


async def test_show_user_roles(make_request, superuser_sign_in):
    access_token = superuser_sign_in['access_token']

    user_id = '0a1dc363-806b-4bf9-90f7-358d2a10b3e2'
    response = await make_request('GET', f'/roles/user/{user_id}', headers=dict(Authorization=access_token))
    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) > 0


async def test_add_user_role(make_request, superuser_sign_in):
    access_token = superuser_sign_in['access_token']

    user_id = '0a1dc363-806b-4bf9-90f7-358d2a10b3e2'
    response = await make_request(
        'POST',
        f'/roles/user/{user_id}',
        payload=dict(name='role_name'),
        headers=dict(Authorization=access_token)
    )
    assert response['status'] == HTTPStatus.OK
