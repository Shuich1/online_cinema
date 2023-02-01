from http import HTTPStatus

import pytest

from ..testdata.es_data import movies_data
from ..testdata.response_models import Film

@pytest.mark.asyncio
async def test_get_all_filmworks(make_get_request):
    response = await make_get_request('/films/', params={'sort': 'imdb_rating'})

    first_film = response['json'][0]
    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) == 10
    assert first_film['imdb_rating'] == 7.5
    assert first_film['title'] == 'The Avengers'

@pytest.mark.asyncio
async def test_get_all_filmworks_descending(make_get_request):
    response = await make_get_request('/films/', params={'sort': '-imdb_rating'})

    first_film = response['json'][0]
    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) == 10
    assert first_film['imdb_rating'] == 9.5
    assert first_film['title'] == 'Gentelmen of Fortune'

@pytest.mark.asyncio
async def test_get_all_filmworks_with_filter(make_get_request):
    response = await make_get_request('/films/', params={'filter[genre]': '111', 'sort': 'imdb_rating', 'page[size]': 50})

    first_film = response['json'][0]
    last_film = response['json'][-1]
    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) == 30
    assert first_film['imdb_rating'] == 7.5
    assert first_film['title'] == 'The Avengers'
    assert last_film['imdb_rating'] == 8.5
    assert last_film['title'] == 'The Star'

@pytest.mark.asyncio
async def test_get_filmwork_by_id(make_get_request):
    response = await make_get_request('/films/1')
    original = movies_data[-1]

    assert response['status'] == HTTPStatus.OK
    assert response['json']['title'] == original['title']
    assert response['json']['imdb_rating'] == original['imdb_rating']
    assert response['json']['description'] == original['description']
    assert response['json']['genre'] == original['genre']
    assert response['json']['director'] == original['director']
    assert response['json']['actors_names'] == original['actors_names']
    assert response['json']['writers_names'] == original['writers_names']
    assert response['json']['actors'] == original['actors']
    assert response['json']['writers'] == original['writers']

@pytest.mark.asyncio
async def test_filmworks_pagination(make_get_request):
    response = await make_get_request('/films/', params={'page[number]': 2, 'page[size]': 5})

    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) == 5

@pytest.mark.asyncio
async def test_filmworks_cache(redis_client, make_get_request):
    response = await make_get_request('/films/1')
    data = await redis_client.get('film_id_1')

    assert response['status'] == HTTPStatus.OK
    assert data is not None
    data = Film.parse_raw(data)
    assert data.title == response['json']['title']
    assert data.imdb_rating == response['json']['imdb_rating']
    assert data.description == response['json']['description']
    assert data.genre == response['json']['genre']
    assert data.director == response['json']['director']
    assert data.actors_names == response['json']['actors_names']
    assert data.writers_names == response['json']['writers_names']
    assert data.actors == response['json']['actors']
    assert data.writers == response['json']['writers']
