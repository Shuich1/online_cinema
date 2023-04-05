import uuid

from src.models.base import BaseOrjsonModel


class ViewInfo(BaseOrjsonModel):
    user_id: uuid
    film_id: str
    viewed: int
