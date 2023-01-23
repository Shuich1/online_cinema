import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .api.v1 import films, genre, person
from .core.config import settings
from .db import elastic, redis

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
    redis.redis = await aioredis.create_redis_pool(
        (settings.redis_host, settings.redis_port),
        minsize=10,
        maxsize=20
    )
    elastic.es = AsyncElasticsearch(
        hosts=[f'{settings.elastic_host}:{settings.elastic_port}']
    )


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genre.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(person.router, prefix='/api/v1/persons', tags=['persons'])
