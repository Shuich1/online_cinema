from http import HTTPStatus


async def test_create_role(make_post_request):
    response = await make_post_request(
        '/roles/role',
        payload=dict(name='reader'),
        headers=dict(Authorization='1234')
    )
    assert response['status'] == HTTPStatus.OK


async def test_get_roles(make_get_request):
    response = await make_get_request('/roles', headers=dict(Authorization='1234'))
    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) > 0


async def test_show_user_roles(make_get_request):
    user_id = '0a1dc363-806b-4bf9-90f7-358d2a10b3e2'
    response = await make_get_request(f'/roles/user/{user_id}', headers=dict(Authorization='1234'))
    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) > 0


async def test_add_user_role(make_post_request):
    user_id = '0a1dc363-806b-4bf9-90f7-358d2a10b3e2'
    response = await make_post_request(
        f'/roles/user/{user_id}',
        payload=dict(name='role_name'),
        headers=dict(Authorization='1234')
    )
    assert response['status'] == HTTPStatus.OK
