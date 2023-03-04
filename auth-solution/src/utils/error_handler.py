from flask import json
from werkzeug.exceptions import HTTPException

from .trace_functions import traced


@traced
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
    response.content_type = "application/json"
    return response
