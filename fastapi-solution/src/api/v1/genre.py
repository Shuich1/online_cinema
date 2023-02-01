from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.genre import Genre
from src.services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get(
    '/',
    response_model=list[Genre],
    summary='All genres',
    description='Returns all genres'
)
async def genres(
    genre_service: GenreService = Depends(get_genre_service),
    size: Optional[int] = Query(
        default=10,
        description='Limit the number of results',
        alias='page[size]'
    ),
) -> list[Genre]:
    genres = await genre_service.get_all(size)
    return genres


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary='Genre details',
    description='Returns genre details by genre uuid'
)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='genre not found'
        )

    return Genre(**genre.dict())
