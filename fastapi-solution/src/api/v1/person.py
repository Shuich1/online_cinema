from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.person import Person
from src.services.person import PersonService, get_person_service
from ...services.jwt_handler import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer(auto_error=False)


@router.get(
    '/search',
    response_model=list[Person],
    summary='Search for persons',
    description='Returns all persons with search query match'
)
async def persons_search(
    person_service: PersonService = Depends(get_person_service),
    jwt_data: JWTBearer = Depends(jwt_bearer),
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
    user_roles = jwt_data['roles']
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
    summary='Person details',
    description='Get person details by person uuid'
    )
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    jwt_data: JWTBearer = Depends(jwt_bearer),
) -> Person:
    user_roles = jwt_data['roles']
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
    description='Get person films details by person uuid'
    )
async def person_films(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    jwt_data: JWTBearer = Depends(jwt_bearer)
) -> list[dict]:
    user_roles = jwt_data['roles']
    films = await person_service.get_films_by_id(person_id)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Person is not found'
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
    jwt_data: JWTBearer = Depends(jwt_bearer),
    page: Optional[int] = Query(
        default=1,
        description='Page number of results',
        alias='page[number]'
    ),
    size: Optional[int] = Query(
        default=10,
        description='Limit the number of results',
        alias='size'
    )
) -> list[Person]:
    user_roles = jwt_data['roles']
    results = await person_service.get_all(page, size)
    if not results:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Persons are not found'
        )
    return results
