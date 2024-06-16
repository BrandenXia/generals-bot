import asyncio
from collections.abc import Callable


def is_async[F: Callable](func: F) -> bool:
    """Check if a function is async"""
    return asyncio.iscoroutinefunction(func)
