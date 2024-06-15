import logging
import time
from collections.abc import Callable, Awaitable
from typing import cast

from .async_utils import is_async

logger = logging.getLogger(__name__)


def timeit[**P, R](func: Callable[P, R]) -> Callable[P, R | Awaitable[R]]:
    """Decorator to measure the time taken by a function to execute"""

    if is_async(func):

        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.monotonic_ns()
            result = await cast(Callable[P, Awaitable[R]], func)(*args, **kwargs)
            logger.debug(f"{func.__name__} took {time.monotonic_ns() - start} seconds")
            return result

        return async_wrapper

    else:

        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.monotonic_ns()
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} took {time.monotonic_ns() - start} seconds")
            return result

        return sync_wrapper
