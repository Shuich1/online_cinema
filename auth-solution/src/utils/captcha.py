from functools import wraps
from http import HTTPStatus

import requests
from flask import jsonify, request
from src.core.config import settings

from .trace_functions import traced


@traced()
def validate_recaptcha(response):
    data = {'secret': settings.reCAPTCHA.RECAPTCHA_SECRET_KEY, 'response': response}

    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    print(response.content)
    if not response.json().get('success'):
        raise ValueError('Invalid CAPTCHA')


def require_recaptcha(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if settings.reCAPTCHA.RECAPTCHA_ENABLED:
            response = request.form.get('g-recaptcha-response')
            if not response:
                return jsonify({'error': 'No CAPTCHA response provided.'}), HTTPStatus.BAD_REQUEST

            try:
                validate_recaptcha(response)
            except ValueError:
                return jsonify({'error': 'Invalid CAPTCHA. Please try again.'}), HTTPStatus.BAD_REQUEST

        return func(*args, **kwargs)
    return inner
