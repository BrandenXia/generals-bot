import logging
import time
from collections.abc import Callable

from .async_utils import is_async


logger = logging.getLogger(__name__)


def timeit[FuncType: Callable](func: FuncType) -> FuncType:
    if is_async:

        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            logger.debug(f"{func.__name__} took {time.time() - start} seconds")
            return result

    else:

        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} took {time.time() - start} seconds")
            return result

    return wrapper
