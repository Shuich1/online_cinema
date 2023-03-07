from functools import wraps
from http import HTTPStatus

import redis
from flask import jsonify, request
from src.core.config import settings
from src.services.redis import redis_rate_limit
from opentelemetry import trace


def rate_limit(
    request_limit=settings.DEFAULT_RATE_LIMIT,
    period=settings.DEFAULT_RATE_PERIOD,
    max_penalty=settings.MAX_RATE_PENALTY
):
    """A decorator that limits the rate of requests to a Flask route using Redis.
    The decorator uses an exponential growth of expiring time after each request that exceeds the set rate limit.

    Args:
        request_limit (int): The maximum number of requests that a client can make within the rate limit period.
        period (int): The duration of the rate limit period in seconds.
        max_penalty(int): Maximum duration of the rate limit penalty in seconds.

    Returns:
        A decorated Flask route function that limits the rate of requests to the route using Redis.
    """

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span("rate-limit-checking"):
                pipeline = redis_rate_limit.pipeline()
                key = f"{request.remote_addr}:{request.path}"
                pipeline.incr(key, 1)
                pipeline.expire(key, period)

                try:
                    request_number = pipeline.execute()[0]
                except redis.exceptions.RedisError:
                    return jsonify(msg=f"Redis error"), HTTPStatus.INTERNAL_SERVER_ERROR

                penalty = 0
                if request_number > request_limit:
                    excess_requests = request_number - request_limit
                    penalty = period * (2 ** (excess_requests - 1))
                    penalty = penalty if penalty < max_penalty else max_penalty

                    pipeline.expire(key, penalty)

                    try:
                        pipeline.execute()
                    except redis.exceptions.RedisError:
                        return jsonify(msg=f"Redis error"), HTTPStatus.INTERNAL_SERVER_ERROR

                    return jsonify(
                        msg="Too many requests",
                        retry_after=penalty
                    ), HTTPStatus.TOO_MANY_REQUESTS

            return func(*args, **kwargs)

        return inner

    return wrapper
