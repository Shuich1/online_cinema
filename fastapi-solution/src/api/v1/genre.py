from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from src.models.genre import Genre
from src.services.genre import GenreService, get_genre_service
from ...services.jwt_handler import JWTBearer

router = APIRouter()
jwt_bearer = JWTBearer(auto_error=False)


@router.get(
    '/',
    response_model=list[Genre],
    summary='All genres',
    description='Returns all genres'
)
async def genres(
    genre_service: GenreService = Depends(get_genre_service),
    jwt_data: JWTBearer = Depends(jwt_bearer),
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
) -> list[Genre]:
    user_roles = jwt_data['roles']
    genres = await genre_service.get_all(page, size)
    return genres


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary='Genre details',
    description='Get genre details by genre uuid'
)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service),
    jwt_data: JWTBearer = Depends(jwt_bearer)
) -> Genre:
    user_roles = jwt_data['roles']
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Genre is not found'
        )

    return Genre(**genre.dict())
