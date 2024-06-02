import asyncio
import logging

from socketio import AsyncClient

from generals_bot.base import BaseListener
from generals_bot.game import GameData
from generals_bot.game.gui import GameGUI
from generals_bot.game.dto import InitialData, UpdateData

logger = logging.getLogger(__name__)


class GameListener(BaseListener):
    _sio: AsyncClient

    def __init__(self, with_gui: bool = True):
        logger.info("GameListener initialized")

        self._sio.on("game_start", self.on_game_start)
        self._sio.on("game_update", self.on_game_update)
        self._sio.on("game_over", self.on_game_over)

        self.data: GameData | None = None

        self.gui: GameGUI | None = GameGUI() if with_gui else None

    async def on_game_start(self, data: InitialData, _):
        logger.info("Game started")
        self.data = GameData(data)

        if self.gui:
            self.gui.set_data(self.data)

    async def on_game_update(self, data: UpdateData, _):
        logger.info("Game updated")
        self.data.update(data)

        if self.gui:
            self.gui.update()

    async def on_game_over(self, _, __):
        logger.info("Game over")
        self.data = None

        await asyncio.sleep(5)
        if self.gui:
            self.gui.reset()
