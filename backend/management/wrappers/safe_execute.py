import asyncio
import logging
from functools import wraps
from reprlib import repr as safe_repr

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
            try:
                args_info = f'with args:\n{safe_repr(args)}\n' if args else ''
                kwargs_info = f'with kwargs:\n{safe_repr(kwargs)}\n' if kwargs else ''
                info = 'and '.join(info for info in (args_info, kwargs_info) if info)
            except Exception:
                info = '(Error retrieving arguments info for logging)'
            if asyncio.iscoroutinefunction(func):
                async def async_wrapper(*args, **kwargs):
                    if settings.SAFE_EXECUTE:
                        try: return await func(*args, **kwargs)
                        except Exception as exc:
                            logger.exception(
                                f'Exception {exc.__class__.__name__} in {func.__name__}\n{info}'
                                f'{func.__code__.co_filename}\nhas been raised:', exc_info=True)

                        if callable(default_value): return default_value(*args_, **kwargs_)
                        return default_value
                    return await func(*args, **kwargs)
                return async_wrapper(*args, **kwargs)
            if settings.SAFE_EXECUTE:
                try: return func(*args, **kwargs)
                except Exception as exc:
                    logger.exception(
                        f'Exception {exc.__class__.__name__} in {func.__name__}\n{info}'
                        f'{func.__code__.co_filename}\nhas been raised:', exc_info=True)

                if callable(default_value): return default_value(*args_, **kwargs_)
                return default_value
            return func(*args, **kwargs)
        return wrapper
    return decorator


@safe_execute('test')
def do_test(test, test_=None):
    raise ValueError(test, test_)
