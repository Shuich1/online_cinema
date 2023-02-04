from typing import Optional

from src.models.base import BaseOrjsonModel
class Film(BaseOrjsonModel):
    id: str
    title: str
    description: Optional[str]
    genre: Optional[list[str]]
    genres: Optional[list[dict[str, str]]]
    imdb_rating: Optional[float]
    director: Optional[list[str]]
    actors: Optional[list[dict[str, str]]]
    writers: Optional[list[dict[str, str]]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
