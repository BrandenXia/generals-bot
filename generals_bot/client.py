import logging
from collections import defaultdict
from collections.abc import Mapping
from typing import Any

from rich.logging import RichHandler

from generals_bot.base import BasePlugin, Namespace
from generals_bot.commands import Generals, Playback
from generals_bot.types.endpoints import ServerType


class GeneralsClient(Generals, Playback):
    """Client for the Generals.io game, with support for plugins"""

    def __init__(
        self,
        user_id: str,
        username: str,
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

        super().__init__(user_id, username, server)

        self._namespaces: Mapping[str, Namespace] = defaultdict(
            lambda: Namespace(self._sio)
        )
        for plugin in plugins or []:
            self._namespaces[plugin.namespace].add_plugin(plugin)

        for namespace in self._namespaces.values():
            namespace.register_plugins()

    async def __aenter__(self) -> "GeneralsClient":
        await self.connect()
        return self

    async def __aexit__(self, _: Any, __: Any, ___: Any) -> None:
        await self.disconnect()
