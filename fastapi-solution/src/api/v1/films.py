from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query
from models.film import Film
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/',
    response_model=list[Film],
    summary='All films',
    description='Returns all films'
)
async def films(
    film_service: FilmService = Depends(get_film_service),
    sort: Union[str, None] = Query(
        None,
        description='Sort by something like imdb_rating',
        alias='sort'
    ),
    genre: Union[str, None] = Query(
        None,
        description='Filter by genre uuid',
        alias='filter[genre]'
    ),
    size: Union[int, None] = Query(
        None,
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


@router.get('/{film_id}', response_model=Film)
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
