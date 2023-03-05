import asyncio
from functools import wraps

from opentelemetry import trace


def traced(func):
    if not asyncio.iscoroutinefunction(func):
        @wraps(func)
        def inner(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(func.__name__):
                return func(*args, **kwargs)
    else:
        @wraps(func)
        async def inner(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(func.__name__):
                return await func(*args, **kwargs)
    return inner
