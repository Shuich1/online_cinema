from functools import lru_cache
from typing import Optional, Union

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

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
        sort: Union[str, None],
        genre: Union[str, None],
        size: Union[int, None] = 10
    ) -> list[Film]:
        try:
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

            res = await self.elastic.search(
                index='movies',
                body={
                    'query': query,
                },
                sort=sort,
                size=size,
            )
            return [Film(**hit['_source']) for hit in res['hits']['hits']]
        except NotFoundError:
            return []

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(f'film_id_{film.id}')
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(
            f'film_id_{film.id}',
            film.json(),
            expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
