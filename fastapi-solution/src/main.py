import aioredis
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from .api.v1 import auth, films, genre, person
from .core.config import settings
from .db import auth_storage, cache, data_storage
from .services.tracer import configure_tracer

app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

if settings.tracer.TRACER_ENABLED:
    configure_tracer()
    FastAPIInstrumentor.instrument_app(app, excluded_urls="/")

    @app.middleware("http")
    async def request_id_checking(request: Request, call_next):
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            raise RuntimeError('Request id is required')

        if request_id != "healthcheck":
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(request.url.path) as span:
                span.set_attribute('http.request_id', request_id)
                return await call_next(request)

        return await call_next(request)        

@app.on_event('startup')
async def startup():
    cache.cache = cache.RedisCache(
        redis=await aioredis.create_redis_pool(
            (settings.redis_host, settings.redis_port),
            db=0,
            minsize=10,
            maxsize=20
        )
    )

    data_storage.data_storage = data_storage.ElasticStorage(
        elastic=[f'{settings.elastic_host}:{settings.elastic_port}']
    )

    auth_storage.auth_storage = auth_storage.RedisAuthStorage(
        redis=await aioredis.create_redis_pool(
            (settings.redis_host, settings.redis_port),
            db=0
        )
    )


@app.on_event('shutdown')
async def shutdown():
    await cache.cache.close()
    await data_storage.data_storage.close()
    await auth_storage.auth_storage.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genre.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(person.router, prefix='/api/v1/persons', tags=['persons'])
app.include_router(auth.router, prefix='/api/v1/signin', tags=['auth'])
