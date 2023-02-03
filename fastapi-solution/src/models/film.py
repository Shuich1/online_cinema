from typing import Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Film(BaseModel):
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

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
