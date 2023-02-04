from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from src.db.elastic import get_elastic
from src.db.cache import get_cache, Cache
from src.models.genre import Genre


class GenreService:
    def __init__(self, cache: Cache, elastic: AsyncElasticsearch):
        self.cache = cache
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None

            await self._put_genre_to_cache(genre)

        return genre

    async def get_all(self, page_number, size: Optional[int]) -> Optional[list[Genre]]:
        try:
            page = await self.elastic.search(
                index='genres',
                body={'query': {'match_all': {}}},
                size=size,
                scroll='2m',
            )
        except NotFoundError:
            return []

        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

        if page_number > 1:
            for i in range(page_number - 1):
                page = await self.elastic.scroll(
                    scroll_id=scroll_id,
                    scroll='2m'
                )
                scroll_id = page['_scroll_id']
                hits = page['hits']['hits']

        return [Genre(**hit['_source']) for hit in hits]

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.cache.get(f'genre_id:{genre_id}')
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.cache.set(
            f'genre_id:{genre.id}',
            genre.json()
        )


@lru_cache()
def get_genre_service(
        cache: Cache = Depends(get_cache),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache, elastic)
