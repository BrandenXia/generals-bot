import logging

from rich.logging import RichHandler

from generals_bot.base import BaseClient, BasePlugin


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

        self.plugins = plugins or []

        [self.register_plugin(plugin) for plugin in self.plugins]

    def register_plugin(self, plugin: BasePlugin):
        assert isinstance(plugin, BasePlugin)
        plugin.set_sio(self._sio)

    async def run(self):
        await self.connect()
        await self.join_private("test", force_start=True)
        await self.wait()
