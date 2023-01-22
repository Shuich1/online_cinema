from typing import Optional

import orjson

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class Serial(BaseModel):
    id: str
    title: str
    description: Optional[str]
    genre: Optional[list[str]]
    # created: datetime.datetime
    imdb_rating: Optional[float]
    director: Optional[str]
    actors: Optional[list[dict[str, str]]]
    writers: Optional[list[dict[str, str]]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    # poster: Optional[str]

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps
