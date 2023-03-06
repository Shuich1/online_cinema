from functools import lru_cache
from typing import Optional

from fastapi import Depends
from src.core.trace_functions import traced
from src.db.cache import Cache, get_cache
from src.db.data_storage import DataStorage, get_data_storage
from src.models.person import Person
from src.services.film import FilmService
from src.services.service import BaseService


class PersonService(BaseService):
    def __init__(self, cache: Cache, data_storage: DataStorage):
        super().__init__(cache, data_storage)

    @traced
    async def get_all(self,
                      page_number: Optional[int],
                      size: Optional[int]
                      ) -> Optional[list[Person]]:
        body = {
                'query': {
                        'match_all': {}
                },
        }
        return await self._search(index='persons',
                                  body=body,
                                  page_number=page_number,
                                  size=size,
                                  model=Person)

    @traced
    async def search(self,
                     query: str,
                     page_number: Optional[int],
                     size: Optional[int],
                     ) -> list[Optional[dict]]:
        fields = [k for k, v in Person.__fields__.items() if v.type_ == str]

        body = {
                'query': {
                        'multi_match': {
                                'query': query,
                                'fields': fields
                        }
                }
        }
        return await self._search(index='persons',
                                  body=body,
                                  page_number=page_number,
                                  size=size,
                                  model=Person)

    @traced
    async def get_by_id(self, uuid: str) -> Optional[Person]:
        data = await self._get_data_from_cache(name_id='person_id',
                                               uuid=uuid,
                                               model=Person)
        if not data:
            data = await self._get_data_from_storage(index='persons',
                                                     uuid=uuid,
                                                     model=Person)
            if not data:
                return None
            await self._put_data_to_cache(name_id='person_id',
                                          data=data)

        return data

    @traced
    async def get_films_by_id(self, person_id: str) -> Optional[list[dict]]:
        films = FilmService(self.cache, self.data_storage)
        person = await self.get_by_id(person_id)
        if person:
            films_info = [await films.get_by_id(film_id)
                          for film_id in person.film_ids]
            return [{'uuid': info.id,
                     'title': info.title,
                     'imdb_rating': info.imdb_rating} for info in films_info]
        return []


@lru_cache()
def get_person_service(
        cache: Cache = Depends(get_cache),
        data_storage: DataStorage = Depends(get_data_storage),
) -> PersonService:
    return PersonService(cache, data_storage)
