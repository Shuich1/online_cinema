from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.person import PersonService, get_person_service

router = APIRouter()


class Person(BaseModel):
    id: str
    full_name: str
    roles: Optional[list[str]]
    film_ids: Optional[list[str]]


@router.get('/{person_id}', response_model=Person)
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='person not found'
        )

    return Person(**person.dict())


@router.get('/', response_model=list[Person])
async def persons(
    person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    results = await person_service.get_all()
    if not persons:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='persons not found'
        )
    return results
