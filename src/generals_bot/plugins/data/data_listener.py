import logging

from generals_bot.base import BasePlugin
from generals_bot.types.dto import InitialData, UpdateData
from .game_data import GameData

logger = logging.getLogger(__name__)


class DataListener(BasePlugin):
    """
    Plugin that listens to game data events and updates the game data.
    Data is stored in the namespace_data dictionary under the key "data"
    """

    @property
    def namespace(self) -> str:
        return "game"

    async def on_game_start(self, data: InitialData, _) -> None:
        logger.info("Game started")
        self._namespace_data["data"] = GameData(data)

    async def on_game_update(self, data: UpdateData, _) -> None:
        logger.info("Game updated")
        self._namespace_data["data"].update(data)

    async def on_game_over(self, _, __) -> None:
        logger.info("Game over")
        self._namespace_data["data"] = None
