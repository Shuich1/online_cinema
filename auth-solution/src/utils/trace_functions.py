from opentelemetry import trace


def traced(func):
    def inner(*args, **kwargs):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(func.__name__):
            return func(*args, **kwargs)
    return inner
