from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from ...models.film import Film
from ...services.film import FilmService, get_film_service
from ...services.jwt_handler import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer(auto_error=False)


@router.get(
    '/search',
    response_model=list[dict],
    summary='Search for films',
    description='Returns all films with search query match'
)
async def films_search(
    film_service: FilmService = Depends(get_film_service),
    jwt_data: JWTBearer = Depends(jwt_bearer),
    query: str = Query(
        default=None,
        description='Film search query',
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
) -> list[dict]:
    if not query:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Search query is missing'
        )
    user_roles = jwt_data['roles']
    results = await film_service.search(query, page, size)
    if not results:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Films are not found'
        )
    return results


@router.get(
    '/',
    response_model=list[Film],
    summary='All films',
    description='Returns all films, optionally filtered by genre and sorted by something like imdb_rating'
)
async def films(
    film_service: FilmService = Depends(get_film_service),
    jwt_data: JWTBearer = Depends(jwt_bearer),
    sort: Optional[str] = Query(
        default=None,
        description='Sort by something like imdb_rating',
        alias='sort'
    ),
    genre: Optional[str] = Query(
        default=None,
        description='Filter by genre uuid',
        alias='filter[genre]'
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
    ),

) -> list[Film]:
    user_roles = jwt_data['roles']
    films = await film_service.get_all(sort, genre, page, size)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Films are not found'
        )
    return films


@router.get(
    '/{film_id}',
    response_model=Film,
    summary='Film details',
    description='Get film details by film uuid'
    )
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service),
    jwt_data: JWTBearer = Depends(jwt_bearer),
) -> Film:
    user_roles = jwt_data['roles']
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Film is not found'
        )

    return Film(**film.dict())
