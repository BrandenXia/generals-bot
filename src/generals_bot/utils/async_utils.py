import asyncio
from collections.abc import Callable


def is_async[**P, R](func: Callable[P, R]) -> bool:
    """Check if a function is async"""
    return asyncio.iscoroutinefunction(func)
