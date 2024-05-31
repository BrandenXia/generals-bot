import logging

from socketio import AsyncClient

from generals_bot.base import BaseListener
from generals_bot.game import GameData
from generals_bot.game.types import InitialData, UpdateData

logger = logging.getLogger(__name__)


class GameListener(BaseListener):
    _sio: AsyncClient

    def __init__(self):
        logger.info("GameListener initialized")

        self._sio.on("game_start", self.on_game_start)
        self._sio.on("game_update", self.on_game_update)

        self.data: GameData | None = None

    async def on_game_start(self, data: InitialData, _):
        logger.info("Game started")
        self.data = GameData(data)

    async def on_game_update(self, data: UpdateData, _):
        logger.info("Game updated")
        self.data.update(data)
