from functools import lru_cache
from typing import Optional

from fastapi import Depends
from src.core.trace_functions import traced
from src.db.cache import Cache, get_cache
from src.db.data_storage import DataStorage, get_data_storage
from src.models.genre import Genre
from src.services.service import BaseService


class GenreService(BaseService):
    def __init__(self, cache: Cache, data_storage: DataStorage):
        super().__init__(cache, data_storage)

    @traced()
    async def get_all(self,
                      page_number: Optional[int],
                      size: Optional[int]) -> Optional[list[Genre]]:
        body = {
                'query': {
                        'match_all': {}
                },
        }
        return await self._search(index='genres',
                                  body=body,
                                  page_number=page_number,
                                  size=size,
                                  model=Genre)

    @traced()
    async def get_by_id(self, uuid: str) -> Optional[Genre]:
        data = await self._get_data_from_cache(name_id='genre_id',
                                               uuid=uuid,
                                               model=Genre)
        if not data:
            data = await self._get_data_from_storage(index='genres',
                                                     uuid=uuid,
                                                     model=Genre)
            if not data:
                return None
            await self._put_data_to_cache(name_id='genre_id',
                                          data=data)

        return data


@lru_cache()
def get_genre_service(
        cache: Cache = Depends(get_cache),
        data_storage: DataStorage = Depends(get_data_storage),
) -> GenreService:
    return GenreService(cache, data_storage)
