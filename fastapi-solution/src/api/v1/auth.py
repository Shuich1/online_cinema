from aioredis import Redis
from fastapi import APIRouter, Depends, Request, Header, Body

from src.services.auth import AuthService, get_auth_service


router = APIRouter()


@router.post(
    '/',
    summary='Sign in router to post',
    description='Sign in router to post',
    )
async def signin(
    user_data: dict = Body(...),
    Authorization: str = Header(...),
    auth_service = Depends(get_auth_service)
):
    response = await auth_service.signin(
        header=Authorization,
        user_data=user_data
    )

    return response
