import asyncio
import logging
from functools import wraps

logger = logging.getLogger('django')

__all__ = ['safe_execute', 'logger']


def safe_execute(default_value=None, *args_, **kwargs_):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                async def async_wrapper(*args, **kwargs):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as exception:
                        logger.exception(exception)
                        if callable(default_value):
                            return default_value(*args_, **kwargs_)
                        return default_value
                return async_wrapper(*args, **kwargs)
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                logger.exception(exception)
                if callable(default_value):
                    return default_value(*args_, **kwargs_)
                return default_value
        return wrapper
    return decorator
