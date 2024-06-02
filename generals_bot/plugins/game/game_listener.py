import asyncio
import logging

from generals_bot.base import BasePlugin
from generals_bot.plugins.game import GameData
from generals_bot.plugins.game.dto import InitialData, UpdateData
from generals_bot.plugins.game.gui import GameGUI

logger = logging.getLogger(__name__)


class GameListener(BasePlugin):
    def __init__(self, with_gui=False):
        super().__init__()

        self.data: GameData | None = None

        self.gui: GameGUI | None = GameGUI() if with_gui else None

    def _register_events(self):
        self._sio.on("game_start", self.on_game_start)
        self._sio.on("game_update", self.on_game_update)
        self._sio.on("game_over", self.on_game_over)

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
