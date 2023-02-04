from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from src.db.cache import get_cache, Cache
from src.db.data_storage import get_data_storage, DataStorage
from src.models.film import Film


class FilmService:
    def __init__(self, cache: Cache, data_storage: DataStorage):
        self.cache = cache
        self.data_storage = data_storage

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def get_all(
        self,
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
                            'must': [
                                {
                                    'match': {
                                        'genres.id': genre
                                    }
                                }
                            ]
                        }
                    }
                }
            }

        sort = sort[1:] + ':desc' if sort and sort.startswith('-') else sort
        try:
            page = await self.data_storage.search(
                index='movies',
                body={
                    'query': query,
                },
                sort=sort,
                size=size,
                scroll='2m'
            )
        except NotFoundError:
            return []

        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

        if page_number > 1:
            for _ in range(1, page_number):
                page = await self.data_storage.scroll(
                    scroll_id=scroll_id,
                    scroll='2m'
                )
                scroll_id = page['_scroll_id']
                hits = page['hits']['hits']

        return [Film(**hit['_source']) for hit in hits]

    async def search(
        self,
        query: str,
        page_number: Optional[int],
        size: Optional[int]
    ) -> list[Optional[dict]]:

        body = {
                'query': {
                        'multi_match': {
                                'query': query,
                                'fields': [f for f in list(Film.__fields__.keys())
                                           if 'imdb_rating' not in f]

                        }
                }
        }
        try:
            page = await self.data_storage.search(
                    index='movies',
                    body=body,
                    size=size,
                    scroll='2m'
            )
        except NotFoundError:
            return []

        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

        if page_number > 1:
            for _ in range(1, page_number):
                page = await self.data_storage.scroll(scroll_id=scroll_id,
                                                    scroll='2m')
                scroll_id = page['_scroll_id']
                hits = page['hits']['hits']

        return [Film(**hit['_source']) for hit in hits]

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.data_storage.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.cache.get(f'film_id:{film_id}')
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.cache.set(
            f'film_id:{film.id}',
            film.json(),
        )


@lru_cache()
def get_film_service(
        cache: Cache = Depends(get_cache),
        elastic: AsyncElasticsearch = Depends(get_data_storage),
) -> FilmService:
    return FilmService(cache, elastic)
