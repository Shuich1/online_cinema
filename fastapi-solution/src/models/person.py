from typing import Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Person(BaseModel):
    id: str
    full_name: str
    roles: Optional[list[str]]
    film_ids: Optional[list[str]]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
