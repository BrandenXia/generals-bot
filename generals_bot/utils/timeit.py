import logging
import time
from collections.abc import Callable

from .async_utils import is_async

logger = logging.getLogger(__name__)


def timeit[FuncType: Callable](func: FuncType) -> FuncType:
    """Decorator to measure the time taken by a function to execute"""

    async def wrapper(*args, **kwargs):
        start = time.time()
        result = (
            (await func(*args, **kwargs)) if is_async(func) else func(*args, **kwargs)
        )
        logger.debug(f"{func.__name__} took {time.time() - start} seconds")
        return result

    return wrapper
