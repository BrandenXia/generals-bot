import asyncio
from collections.abc import Callable


def is_async(func: Callable) -> bool:
    return asyncio.iscoroutinefunction(func)
