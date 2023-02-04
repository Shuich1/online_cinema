import logging
import os
from logging import config as logging_config

from settings import test_settings

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': test_settings.logging_level,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': test_settings.logging_level,
        },
        'uvicorn.error': {
            'level': test_settings.logging_level,
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': test_settings.logging_level,
            'propagate': False,
        },
    },
    'root': {
        'level': test_settings.logging_level,
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}

logging_config.dictConfig(LOGGING)

def get_logger(name: str) -> logging.Logger:
    """
    Функция для получения логгера
    Args:
        name: имя логгера
    Returns:
        logger: логгер
    """
    if not os.path.exists('logs'):
        os.mkdir('logs')

    logging.config.dictConfig(LOGGING)
    return logging.getLogger(name)