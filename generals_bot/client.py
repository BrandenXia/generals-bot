import logging
from collections import defaultdict
from collections.abc import Mapping

from rich.logging import RichHandler

from generals_bot.base import BaseClient, BasePlugin, Namespace


class GeneralsClient(BaseClient):
    def __init__(
        self,
        user_id: str,
        username: str,
        server,
        plugins: list[BasePlugin] | None = None,
        debug: bool = False,
    ):
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

    async def run(self):
        await self.connect()
        await self.join_private("test", force_start=True)
        await self.wait()
