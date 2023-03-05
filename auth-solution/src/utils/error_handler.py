from flask import json
from werkzeug.exceptions import HTTPException

from opentelemetry import trace


def handle_exception(ex: HTTPException):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = ex.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": ex.code,
        "error": ex.name,
        "message": ex.description,
    })

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span(__name__) as span:
        span.set_attribute('http.status', ex.code)
        span.set_attribute('http.error', ex.name)
        span.set_attribute('http.error_message', ex.description)
        
    response.content_type = "application/json"
    return response
