import json
from http import HTTPStatus

import pytest
from deepdiff import DeepDiff

from ..testdata.es_data import default_size, genres_data


@pytest.mark.asyncio
async def test_get_all_genres(make_get_request):
    response = await make_get_request('/genres/')

    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) == default_size


@pytest.mark.asyncio
async def test_get_all_genres_with_size(make_get_request):
    response = await make_get_request('/genres/', params={'page[size]': 45})

    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) == 45


@pytest.mark.asyncio
@pytest.mark.parametrize('genre_id, status, details', [
    (
        genres_data[0]['id'],
        HTTPStatus.OK,
        genres_data[0],
    ),
    (
        'a288e9cb-b11a-451f-80cb-111111111',
        HTTPStatus.NOT_FOUND,
        None,
    ),
])
async def test_get_one_genre(make_get_request, genre_id, status, details):
    response = await make_get_request(f'/genres/{genre_id}')

    assert response['status'] == status
    if details:
        assert not DeepDiff(response['json'], details)


@pytest.mark.asyncio
@pytest.mark.parametrize('genre_id, status', [
    (
        genres_data[0]['id'],
        HTTPStatus.OK,
    ),
])
async def test_get_one_genre_from_cache(
    redis_client,
    make_get_request,
    genre_id,
    status
):
    response = await make_get_request(f'/genres/{genre_id}')
    redis_data = await redis_client.get(f'genre_id:{genre_id}')

    assert response['status'] == status
    assert redis_data is not None
    assert not DeepDiff(json.loads(redis_data), response['json'])
