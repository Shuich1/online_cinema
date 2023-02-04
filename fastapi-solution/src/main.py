import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .api.v1 import films, genre, person
from .core.config import settings
from .db import data_storage, cache

app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    cache.cache = cache.RedisCache(
        redis=await aioredis.create_redis_pool(
            (settings.redis_host, settings.redis_port),
            minsize=10,
            maxsize=20
        )
    )

    data_storage.data_storage = data_storage.ElasticStorage(
        elastic=[f'{settings.elastic_host}:{settings.elastic_port}']
    )


@app.on_event('shutdown')
async def shutdown():
    await cache.cache.close()
    await data_storage.data_storage.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genre.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(person.router, prefix='/api/v1/persons', tags=['persons'])
