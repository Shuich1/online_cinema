from functools import wraps
from http import HTTPStatus

import redis
from flask import jsonify, request
from src.core.config import settings
from src.services.redis import redis_rate_limit
from src.utils.trace_functions import traced


def rate_limit(
    request_limit=settings.DEFAULT_RATE_LIMIT,
    penalty=settings.DEFAULT_RATE_PENALTY,
    max_penalty=settings.MAX_RATE_PENALTY
):
    """A decorator that limits the rate of requests to a Flask route using Redis.
    The decorator uses an exponential growth of expiring time after each request that exceeds the set rate limit.

    Args:
        request_limit (int): The maximum number of requests that a client can make within the rate limit penalty.
        penalty (int): The duration of the rate limit penalty in seconds.
        max_penalty(int): Maximum duration of the rate limit penalty in seconds.

    Returns:
        A decorated Flask route function that limits the rate of requests to the route using Redis.
    """

    def wrapper(func):
        @wraps(func)
        @traced("Rate limit checking")
        def inner(*args, **kwargs):
            pipeline = redis_rate_limit.pipeline()
            key = f"{request.remote_addr}:{request.path}"
            pipeline.incr(key, 1)
            pipeline.expire(key, penalty)

            try:
                request_number = pipeline.execute()[0]
            except redis.exceptions.RedisError:
                return jsonify(msg=f"Redis error"), HTTPStatus.INTERNAL_SERVER_ERROR

            retry_after = 0
            if request_number > request_limit:
                excess_requests = request_number - request_limit
                retry_after = penalty * (2 ** (excess_requests % request_limit - 1))
                retry_after = retry_after if retry_after < max_penalty else max_penalty

                pipeline.expire(key, retry_after)

                try:
                    pipeline.execute()
                except redis.exceptions.RedisError:
                    return jsonify(msg=f"Redis error"), HTTPStatus.INTERNAL_SERVER_ERROR

                return jsonify(
                    msg="Too many requests",
                    retry_after=retry_after
                ), HTTPStatus.TOO_MANY_REQUESTS

            return func(*args, **kwargs)

        return inner

    return wrapper
