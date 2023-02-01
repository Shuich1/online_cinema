from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from src.services.person import PersonService, get_person_service

router = APIRouter()


class Person(BaseModel):
    id: str
    full_name: str
    roles: Optional[list[str]]
    film_ids: Optional[list[str]]


@router.get(
    '/search',
    response_model=list[Person],
    summary='Search for persons',
    description='Returns all persons with search query match'
)
async def persons_search(
    person_service: PersonService = Depends(get_person_service),
    query: str = Query(
        default=None,
        description='Person search query',
        alias='query'
    ),
    page: Optional[int] = Query(
        default=1,
        description='Page number of results',
        alias='page[number]'
    ),
    size: Optional[int] = Query(
        default=10,
        description='Limit the number of results',
        alias='page[size]'
    )
) -> list[Person]:
    if not query:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Search query is missing'
        )
    results = await person_service.search(query, page, size)
    if not results:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Persons are not found'
        )
    return results


@router.get(
    '/{person_id}',
    response_model=Person,
    summary='Search for person by ID',
    description='Returns person details by person uuid'
    )
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Person is not found'
        )

    return Person(**person.dict())


@router.get(
    '/{person_id}/film',
    response_model=list[dict],
    summary='Person film info',
    description='Returns person films details by person uuid'
    )
async def person_films(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> list[dict]:
    films = await person_service.get_films_by_id(person_id)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Person are not found'
        )

    return films


@router.get(
    '/',
    response_model=list[Person],
    summary='All persons',
    description='Returns all persons with films participated in'
)
async def persons(
    person_service: PersonService = Depends(get_person_service),
    size: Optional[int] = Query(
        default=10,
        description='Limit the number of results',
        alias='size'
    )
) -> list[Person]:
    results = await person_service.get_all(size)
    if not results:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Persons are not found'
        )
    return results
