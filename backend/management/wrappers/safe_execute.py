import asyncio
import logging
from functools import wraps

from django.conf import settings

logger = logging.getLogger('django')


def safe_execute(default_value=None, *args_, **kwargs_):
    """
    A wrapper for functions that handles exceptions and logs them. Relevant for synchronous and asynchronous functions.
    In case of an error, it can return the default value, including a function for which you can specify additional
        arguments and key values.
    Important! Do not use it for functions that should throw exceptions, for example, for validators.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                async def async_wrapper(*args, **kwargs):
                    if settings.SAFE_EXECUTE:
                        try:
                            return await func(*args, **kwargs)
                        except Exception as exception:
                            logger.exception(
                                f"Exception in {func.__name__} with args {args}, kwargs {kwargs}: {exception}",
                                exc_info=True)
                            if callable(default_value):
                                return default_value(*args_, **kwargs_)
                            return default_value
                    return await func(*args, **kwargs)
                return async_wrapper(*args, **kwargs)
            if settings.SAFE_EXECUTE:
                try:
                    return func(*args, **kwargs)
                except Exception as exception:
                    logger.exception(
                        f"Exception in {func.__name__} with args {args}, kwargs {kwargs}: {exception}",
                        exc_info=True)
                    if callable(default_value):
                        return default_value(*args_, **kwargs_)
                    return default_value
            return func(*args, **kwargs)
        return wrapper
    return decorator
