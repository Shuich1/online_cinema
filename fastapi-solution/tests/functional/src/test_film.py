from http import HTTPStatus

import pytest
from deepdiff import DeepDiff

from ..testdata.es_data import movies_data
from ..testdata.response_models import Film


@pytest.mark.asyncio
async def test_get_all_filmworks(make_get_request):
    response = await make_get_request('/films/')

    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) == 10


@pytest.mark.asyncio
@pytest.mark.parametrize('size, status', [
    (20, HTTPStatus.OK),
    (35, HTTPStatus.OK),
])
async def test_get_all_filmworks_with_size(make_get_request, size, status):
    response = await make_get_request('/films/', params={'page[size]': size})

    assert response['status'] == status
    assert len(response['json']) == size


@pytest.mark.asyncio
@pytest.mark.parametrize('sort, first_film, status', [
    (
        'imdb_rating',
        movies_data[-1],
        HTTPStatus.OK,
    ),
    (
        '-imdb_rating',
        movies_data[15],
        HTTPStatus.OK,
    ),
])
async def test_get_all_filmworks_sort(make_get_request, sort, first_film, status):
    response = await make_get_request('/films/', params={'sort': sort})

    assert response['status'] == status
    assert len(response['json']) == 10
    assert not DeepDiff(response['json'][0], first_film)


@pytest.mark.asyncio
@pytest.mark.parametrize('genre, first_film, status', [
    (
        '111',
        movies_data[0],
        HTTPStatus.OK,
    ),
    (
        '222',
        movies_data[0],
        HTTPStatus.OK,
    ),
])
async def test_filter_by_genre(make_get_request, genre, first_film, status):
    response = await make_get_request('/films/', params={'filter[genre]': genre})

    assert response['status'] == status
    assert len(response['json']) == 10
    assert not DeepDiff(response['json'][0], first_film)


@pytest.mark.asyncio
@pytest.mark.parametrize('film_id, status, details', [
    (
        movies_data[0]['id'],
        HTTPStatus.OK,
        Film(**movies_data[0]),
    ),
    (
        'a288e9cb-b11a-451f-80cb-111111111',
        HTTPStatus.NOT_FOUND,
        None,
    ),
])
async def test_get_filmwork_by_id(make_get_request, film_id, status, details):
    response = await make_get_request(f'/films/{film_id}')

    assert response['status'] == status
    if details:
        assert not DeepDiff(response['json'], details.dict())


@pytest.mark.asyncio
@pytest.mark.parametrize('page, status', [
    (1, HTTPStatus.OK),
    (2, HTTPStatus.OK),
    (3, HTTPStatus.OK),
])
async def test_get_all_filmworks_with_page(make_get_request, page, status):
    response = await make_get_request('/films/', params={'page[number]': page})

    assert response['status'] == status
    assert len(response['json']) == 10
    assert response['json'][0]['id'] == movies_data[10 * (page - 1)]['id']


@pytest.mark.asyncio
@pytest.mark.parametrize('query, first_film, status', [
    ('Star', movies_data[0], HTTPStatus.OK),
    ('end', movies_data[-1], HTTPStatus.OK),
    ('qwerty', None, HTTPStatus.NOT_FOUND),
])
async def test_search_filmwork(make_get_request, query, first_film, status):
    response = await make_get_request('/films/search', params={'query': query})

    assert response['status'] == status
    print(response['json'])
    print(first_film)

    if first_film:
        assert not DeepDiff(response['json'][0], first_film)


@pytest.mark.asyncio
@pytest.mark.parametrize('film_id, status, details', [
    (
        movies_data[0]['id'],
        HTTPStatus.OK,
        Film(**movies_data[0]),
    ),
    (
        'a288e9cb-b11a-451f-80cb-111111111',
        HTTPStatus.NOT_FOUND,
        None,
    ),
])
async def test_get_filmwork_by_id_with_cache(redis_client, make_get_request, film_id, status, details):
    response = await make_get_request(f'/films/{film_id}')
    redis_data = await redis_client.get(f'film_id:{film_id}')

    assert response['status'] == status
    if details:
        assert redis_data is not None
        assert not DeepDiff(response['json'], Film.parse_raw(redis_data).dict())