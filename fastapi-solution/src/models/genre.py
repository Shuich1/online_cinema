from typing import Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Genre(BaseModel):
    id: str
    name: str
    description: Optional[str]
    rating: Optional[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
