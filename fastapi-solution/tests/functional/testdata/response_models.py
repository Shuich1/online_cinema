from typing import Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


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


class Genre(BaseOrjsonModel):
    id: str
    name: str


class Person(BaseOrjsonModel):
    id: str
    full_name: str
    roles: Optional[list[str]]
    film_ids: Optional[list[str]]
