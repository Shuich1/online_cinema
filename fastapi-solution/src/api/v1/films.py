from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.film import Film
from src.services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/search',
    response_model=list[dict],
    summary='Search for films',
    description='Returns all films with search query match'
)
async def films_search(
    film_service: FilmService = Depends(get_film_service),
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
    size: Optional[int] = Query(
        default=10,
        description='Limit the number of results',
        alias='size'
    )
) -> list[Film]:
    films = await film_service.get_all(sort, genre, size)
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='films not found'
        )
    return films


@router.get(
    '/{film_id}',
    response_model=Film,
    summary='Film details',
    description='Returns film details by film uuid'
    )
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='film not found'
        )

    return Film(**film.dict())
