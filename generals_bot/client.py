import logging
from typing import Literal

from socketio import AsyncClient

from generals_bot.base import BaseClient
from generals_bot.game import GameListener
from generals_bot.global_listener import GlobalListener
from generals_bot.logger import logger


class GeneralsClient(BaseClient, GlobalListener, GameListener):
    _sio = None

    def __init__(
        self,
        user_id: str,
        username: str,
        server: Literal["human", "bot"],
        debug: bool = False,
    ):
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

        self._sio = AsyncClient()

        BaseClient.__init__(self, user_id, username, server)
        GlobalListener.__init__(self)
        GameListener.__init__(self)
