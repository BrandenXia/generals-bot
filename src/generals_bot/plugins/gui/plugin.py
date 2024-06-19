from generals_bot.base import BasePlugin
from .gui import GameGUI


class GUIPlugin(BasePlugin):
    """Plugin for the GUI of the game"""

    @property
    def namespace(self) -> str:
        return "game"

    def __init__(self) -> None:
        super().__init__()
        self.gui = GameGUI()

    async def on_game_start(self, _, __) -> None:
        self.gui.reset()
        self.gui.set_data(self._namespace_data["data"])

    async def on_game_update(self, _, __) -> None:
        self.gui.update()

    async def on_game_over(self, _, __) -> None:
        self.gui.game_over()
