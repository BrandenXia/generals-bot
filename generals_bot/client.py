import logging

from rich.logging import RichHandler
from socketio import AsyncClient

from generals_bot.base import BaseClient
from generals_bot.game import GameListener
from generals_bot.global_listener import GlobalListener


class GeneralsClient(BaseClient, GlobalListener, GameListener):
    _sio = None

    def __init__(
        self,
        user_id: str,
        username: str,
        server,
        debug: bool = False,
    ):
        logging.basicConfig(
            level=logging.DEBUG if debug else logging.INFO,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler()],
        )

        self._sio = AsyncClient()

        BaseClient.__init__(self, user_id, username, server)
        GlobalListener.__init__(self)
        GameListener.__init__(self)

    async def run(self):
        await self.connect()
        await self.join_private("test", force_start=True)
        await self.wait()
