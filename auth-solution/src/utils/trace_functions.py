import asyncio
from functools import wraps

from opentelemetry import trace


def traced(name: str = None):
    """
    A decorator that wraps a function with OpenTelemetry tracing capabilities.

    Args:
        name (str, optional): The name of the span. If provided, it will be used instead of the function name.

    Returns:
        A function that wraps the input function with OpenTelemetry tracing capabilities.

    Usage:
        To use this decorator, simply apply it to the desired function. For example:

        @traced()
        def my_function():
            pass
            
        Or, if you want to specify a custom name for the span:

        @traced(name="my_span")
        def my_function():
            pass
            
        This decorator is designed to work with synchronous and asynchronous functions.
        If the wrapped function is synchronous, it will be executed normally.
        If the wrapped function is asynchronous, it will be awaited.
    """
    def wrapper(func):
        if not asyncio.iscoroutinefunction(func):
            @wraps(func)
            def inner(*args, **kwargs):
                tracer = trace.get_tracer(__name__)
                with tracer.start_as_current_span(func.__name__ if not name else name):
                    return func(*args, **kwargs)
        else:
            @wraps(func)
            async def inner(*args, **kwargs):
                tracer = trace.get_tracer(__name__)
                with tracer.start_as_current_span(func.__name__ if not name else name):
                    return await func(*args, **kwargs)
        return inner
    return wrapper
