import logging
from collections.abc import Callable, Awaitable

from socketio import AsyncClient

logger = logging.getLogger(__name__)


class MultiHandlerAsyncClient(AsyncClient):
    """AsyncClient subclass that allows multiple handlers for the same event"""

    def on[
    ** P
    ](
            self,
            event: str,
            handler: Callable[P, Awaitable[None]] | None = None,
            namespace: str | None = None,
    ) -> (
            Callable[[Callable[P, Awaitable[None]]], Callable[P, Awaitable[None]]] | None
    ):
        """
        Override the on method to allow multiple handlers for the same event,
        note that the handlers are executed in the order they are added.
        """
        namespace = namespace or "/"

        def add_handler(
                new_handler: Callable[P, Awaitable[None]]
        ) -> Callable[P, Awaitable[None]]:
            if namespace not in self.handlers:
                self.handlers[namespace] = {}

            if prev := self.handlers[namespace].get(event):

                async def handler_wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
                    await prev(*args, **kwargs)
                    await new_handler(*args, **kwargs)

                self.handlers[namespace][event] = handler_wrapper
            else:
                self.handlers[namespace][event] = new_handler

            return new_handler

        if handler is None:
            return add_handler

        add_handler(handler)

        return None
