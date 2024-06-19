import logging
from collections import defaultdict
from collections.abc import Mapping, Callable
from typing import Any, Self

from rich.logging import RichHandler

from generals_bot.base import BasePlugin, Namespace, BaseClient
from generals_bot.types.endpoints import ServerType


class GeneralsClient(BaseClient):
    """Client for the Generals.io game, with support for plugins"""

    def __init__(
        self,
        server: ServerType,
        plugins: list[BasePlugin] | None = None,
        debug: bool = False,
    ) -> None:
        logging.basicConfig(
            level=logging.DEBUG if debug else logging.INFO,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler()],
        )

        super().__init__(server)

        self.methods: dict[str, Callable[..., Any]] = {}
        self._namespaces: Mapping[str, Namespace] = defaultdict(
            lambda: Namespace(self._add_method, self._sio)
        )
        for plugin in plugins or []:
            self._namespaces[plugin.namespace].add_plugin(plugin)

        for namespace in self._namespaces.values():
            namespace.register_plugins()

    def _add_method(self, name: str, method: Callable[..., Any]) -> None:
        self.methods[name] = method

    def __getattr__(self, item: str) -> Callable[..., Any] | None:
        return self.methods.get(item)

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, _: Any, __: Any, ___: Any) -> None:
        await self.wait()
