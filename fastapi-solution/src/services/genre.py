from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
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
        page = await self.elastic.search(
            index='genres',
            body={'query': {'match_all': {}}},
            size=size,
            scroll='2m',
        )

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

        results = [Genre(**hit['_source']) for hit in hits]
        return results

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        data = await self.redis.get(f'genre_id:{genre_id}')
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(
            f'genre_id:{genre.id}',
            genre.json(),
            expire=GENRE_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
