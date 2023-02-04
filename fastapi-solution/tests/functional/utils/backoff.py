import asyncio
import time
from functools import wraps

from utils.logger import get_logger

logger = get_logger(__name__)

def backoff(start_time, stop_time, factor):
    """
    Decorator to retry a function if it fails, working with both sync and async functions
    Args:
        start_time: time to sleep before retrying
        stop_time: maximum time to sleep before retrying
        factor: factor to increase sleep time by
    Returns:
        wrapper: wrapper function
    """
    def wrapper(func):
        if not asyncio.iscoroutinefunction(func):
            @wraps(func)
            def inner(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except:
                    t = start_time
                    while True:
                        logger.info(f'Failed to connect. Sleeping {t} seconds and trying again')
                        time.sleep(t)
                        try:
                            return func(*args, **kwargs)
                        except:
                            t = (t * 2 ** factor) if (t * 2 ** factor) < stop_time else stop_time
        else:
            @wraps(func)
            async def inner(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except:
                    t = start_time
                    while True:
                        logger.info(f'Failed to connect. Sleeping {t} seconds and trying again')
                        await asyncio.sleep(t)
                        try:
                            return await func(*args, **kwargs)
                        except:
                            t = (t * 2 ** factor) if (t * 2 ** factor) < stop_time else stop_time
        return inner
    return wrapper
