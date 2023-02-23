from functools import lru_cache
from typing import Optional

from fastapi import Depends
from src.db.cache import Cache, get_cache
from src.db.data_storage import DataStorage, get_data_storage
from src.models.film import Film
from src.services.service import BaseService


class FilmService(BaseService):
    def __init__(self, cache: Cache, data_storage: DataStorage):
        super().__init__(cache, data_storage)

    async def get_all(self,
                      sort: Optional[str],
                      genre: Optional[str],
                      page_number: Optional[int],
                      size: Optional[int]
                      ) -> list[Film]:

        query = {
                'match_all': {}
        }

        if genre:
            query = {
                    'nested': {
                            'path': 'genres',
                            'query': {
                                    'bool': {
                                            'must': [{
                                                    'match': {
                                                            'genres.id': genre
                                                    }
                                            }]
                                    }
                            }
                    }
            }

        body = {
                'query': query,
        }
        sort = sort[1:] + ':desc' if sort and sort.startswith('-') else sort

        return await self._search(index='movies',
                                  body=body,
                                  page_number=page_number,
                                  size=size,
                                  model=Film,
                                  sort=sort)

    async def search(self,
                     query: str,
                     page_number: Optional[int],
                     size: Optional[int],
                     ) -> list[Optional[dict]]:
        # searching upon all sting fields
        fields = [k for k, v in Film.__fields__.items() if v.type_ == str]

        body = {
                'query': {
                        'multi_match': {
                                'query': query,
                                'fields': fields
                        }
                }
        }
        return await self._search(index='movies',
                                  body=body,
                                  page_number=page_number,
                                  size=size,
                                  model=Film)

    async def get_by_id(self, uuid: str) -> Optional[Film]:
        data = await self._get_data_from_cache(name_id='film_id',
                                               uuid=uuid,
                                               model=Film)
        if not data:
            data = await self._get_data_from_storage(index='movies',
                                                     uuid=uuid,
                                                     model=Film)
            if not data:
                return None
            await self._put_data_to_cache(name_id='film_id',
                                          data=data)

        return data


@lru_cache()
def get_film_service(
        cache: Cache = Depends(get_cache),
        data_storage: DataStorage = Depends(get_data_storage),
) -> FilmService:
    return FilmService(cache, data_storage)
