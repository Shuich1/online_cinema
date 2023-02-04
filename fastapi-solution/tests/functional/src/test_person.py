import json
from http import HTTPStatus

import pytest
from deepdiff import DeepDiff

from ..testdata.es_data import persons_data, default_size


DUMMY_PERSON_ID = 'a288e9cb-b11a-451f-80cb-111111111'


@pytest.mark.asyncio
async def test_get_all_persons(make_get_request):
    response = await make_get_request('/persons/')

    assert response['status'] == HTTPStatus.OK
    assert len(response['json']) == default_size


@pytest.mark.asyncio
@pytest.mark.parametrize('params, status, count', [
    (
        {'size': 20},
        HTTPStatus.OK,
        20,
    ),
    (
        {'size': 50},
        HTTPStatus.OK,
        45,
    ),
])
async def test_get_all_persons_with_size(make_get_request, params, status, count):
    response = await make_get_request('/persons/', params=params)

    assert response['status'] == status
    assert len(response['json']) == count


@pytest.mark.asyncio
@pytest.mark.parametrize('person_id, status', [
    (
        persons_data[0]['id'],
        HTTPStatus.OK,
    ),
    (
        persons_data[-1]['id'],
        HTTPStatus.OK,
    ),
    (
        DUMMY_PERSON_ID,
        HTTPStatus.NOT_FOUND,
    ),
])
async def test_get_films_person(make_get_request, person_id, status):
    response = await make_get_request(f'/persons/{person_id}/film/')

    assert response['status'] == status


@pytest.mark.asyncio
@pytest.mark.parametrize('person_id, status, details', [
    (
        persons_data[5]['id'],
        HTTPStatus.OK,
        persons_data[5]
    ),
    (
        persons_data[15]['id'],
        HTTPStatus.OK,
        persons_data[15]
    ),
])
async def test_get_existing_person_details(make_get_request, person_id, status, details):
    response = await make_get_request(f'/persons/{person_id}/')

    assert response['status'] == status
    assert not DeepDiff(details, response['json'], ignore_order=True)


@pytest.mark.asyncio
@pytest.mark.parametrize('person_id, status', [
    (
        persons_data[3]['id'],
        HTTPStatus.OK,
    ),
    (
        persons_data[3]['id'],
        HTTPStatus.OK,
    ),
])
async def test_get_person_details_from_cache(redis_client, make_get_request, person_id, status):
    response = await make_get_request(f'/persons/{person_id}/')
    redis_data = await redis_client.get(f'person_id:{person_id}')

    assert response['status'] == status
    assert redis_data is not None
    assert not DeepDiff(json.loads(redis_data), response['json'], ignore_order=True)


@pytest.mark.asyncio
@pytest.mark.parametrize('person_id, status', [
    (
        DUMMY_PERSON_ID,
        HTTPStatus.NOT_FOUND,
    ),
])
async def test_get_missing_person_details(make_get_request, person_id, status):
    response = await make_get_request(f'/persons/{person_id}/')

    assert response['status'] == status


@pytest.mark.asyncio
@pytest.mark.parametrize('params, status, count', [
    (
        {'query': 'filter[full_name]=Ann Smith', 'page[size]': 30},
        HTTPStatus.OK,
        15
    ),
    (
        {'query': 'filter[roles]=Writer,Actor,', 'page[size]': 45},
        HTTPStatus.OK,
        45
    ),
])
async def test_search_persons(make_get_request, params, status, count):
    response = await make_get_request(f'/persons/search/', params=params)

    assert response['status'] == status
    assert len(response['json']) == count
