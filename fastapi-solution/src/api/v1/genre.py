from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.genre import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    id: str
    name: str


@router.get('/', response_model=list[Genre])
async def all_genres(genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    genres = await genre_service.get_all_rows()

    return [Genre(id=_genre.id, name=_genre.name) for _genre in genres]


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return Genre(id=genre.id, name=genre.name)
