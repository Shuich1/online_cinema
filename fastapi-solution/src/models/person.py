from typing import Optional

from src.models.base import BaseOrjsonModel


class Person(BaseOrjsonModel):
    id: str
    full_name: str
    roles: Optional[list[str]]
    film_ids: Optional[list[str]]
