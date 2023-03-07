import redis
from src.core.config import settings

jwt_redis_blocklist = redis.StrictRedis(
    host=settings.AUTH_REDIS_HOST,
    port=settings.AUTH_REDIS_PORT,
    db=0,
    decode_responses=True
)

jwt_redis_refresh_tokens = redis.StrictRedis(
    host=settings.AUTH_REDIS_HOST,
    port=settings.AUTH_REDIS_PORT,
    db=1,
    decode_responses=True
)

redis_rate_limit = redis.StrictRedis(
    host=settings.AUTH_REDIS_HOST,
    port=settings.AUTH_REDIS_PORT,
    db=2,
    decode_responses=True
)
