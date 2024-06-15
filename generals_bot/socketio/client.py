import logging
from collections.abc import Callable, Awaitable

from socketio import AsyncClient

logger = logging.getLogger(__name__)


class MultiHandlerAsyncClient(AsyncClient):
    """AsyncClient subclass that allows multiple handlers for the same event"""

    def on[
        T
    ](
        self,
        event: str,
        handler: Callable[T, Awaitable[None]] | None = None,
        namespace: str | None = None,
    ) -> (
        Callable[[Callable[T, Awaitable[None]]], Callable[T, Awaitable[None]]] | None
    ):
        """
        Override the on method to allow multiple handlers for the same event,
        note that the handlers are executed in the order they are added.
        """
        namespace = namespace or "/"

        def add_handler(
            new_handler: Callable[T, Awaitable[None]]
        ) -> Callable[T, Awaitable[None]]:
            if namespace not in self.handlers:
                self.handlers[namespace] = {}

            if prev := self.handlers[namespace].get(event):
                prev: Callable[T, Awaitable[None]]

                async def handler_wrapper(*args: T) -> None:
                    await prev(*args)
                    await new_handler(*args)

                self.handlers[namespace][event] = handler_wrapper
            else:
                self.handlers[namespace][event] = new_handler

            return new_handler

        if handler is None:
            return add_handler

        add_handler(handler)

        return None
