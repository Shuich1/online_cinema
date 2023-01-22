from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from models.genre import Genre

from services.genre import GenreService, get_genre_service

router = APIRouter()

@router.get('/', response_model=list[Genre])
async def genres(
    genre_service: GenreService = Depends(get_genre_service),
    size: int = 100,
    ) -> list[Genre]:
    genres = await genre_service.get_all(size)
    return genres


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return Genre(**genre.dict())

