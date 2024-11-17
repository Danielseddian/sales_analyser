import asyncio
import logging
from functools import wraps

logger = logging.getLogger('django')


def safe_execute(default_value=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                async def async_wrapper(*args, **kwargs):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as exception:
                        logger.exception(exception)
                        return default_value
                return async_wrapper(*args, **kwargs)
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                logger.exception(exception)
                return default_value
        return wrapper
    return decorator
