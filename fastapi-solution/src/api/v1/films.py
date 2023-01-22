from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Union

from services.film import FilmService, get_film_service

router = APIRouter()


class Film(BaseModel):
    id: str
    title: str

@router.get(
    '/',
    response_model=list[Film],
    summary='All films',
    description='Returns all films'
)
async def films(
    film_service: FilmService = Depends(get_film_service),
    sort: Union[str, None] = Query(None, description='Sort by something like imdb_rating', alias='sort'),
    genre: Union[str, None] = Query(None, description='Filter by genre uuid', alias='filter[genre]',)
    ) -> list[Film]:
    films = await film_service.get_all(sort, genre)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')
    return films

@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(id=film.id, title=film.title)
