import asyncio
from collections.abc import Callable


def is_async(func: Callable) -> bool:
    """Check if a function is async"""
    return asyncio.iscoroutinefunction(func)
