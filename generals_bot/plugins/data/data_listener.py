import logging

from generals_bot.base import BasePlugin
from .game_data import GameData
from .dto import InitialData, UpdateData

logger = logging.getLogger(__name__)


class DataListener(BasePlugin):
    """
    Plugin that listens to game data events and updates the game data.
    Data is stored in the namespace_data dictionary under the key "data"
    """

    namespace = "game"

    def _register_events(self) -> None:
        self._sio.on("game_start", self.on_game_start)
        self._sio.on("game_update", self.on_game_update)
        self._sio.on("game_over", self.on_game_over)

    async def on_game_start(self, data: InitialData, _) -> None:
        logger.info("Game started")
        self._namespace_data["data"] = GameData(data)

    async def on_game_update(self, data: UpdateData, _) -> None:
        logger.info("Game updated")
        self._namespace_data["data"].update(data)

    async def on_game_over(self, _, __) -> None:
        logger.info("Game over")
        self._namespace_data["data"] = None
