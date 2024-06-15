from generals_bot.base import BasePlugin
from .gui import GameGUI


class GUIPlugin(BasePlugin):
    """Plugin for the GUI of the game"""

    namespace = "game"

    def __init__(self) -> None:
        super().__init__()
        self.gui = GameGUI()

    def _plugin_initialize(self) -> None:
        self._sio.on("game_start", self.on_game_start)
        self._sio.on("game_update", self.on_game_update)
        self._sio.on("game_over", self.on_game_over)

    async def on_game_start(self, _, __) -> None:
        self.gui.reset()
        self.gui.set_data(self._namespace_data["data"])

    async def on_game_update(self, _, __) -> None:
        self.gui.update()

    async def on_game_over(self, _, __) -> None:
        self.gui.game_over()
