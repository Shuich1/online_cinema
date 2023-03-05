from opentelemetry import trace
from functools import wraps
import asyncio


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
