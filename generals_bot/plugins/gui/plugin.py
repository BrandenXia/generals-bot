import asyncio

from generals_bot.base import BasePlugin
from .gui import GameGUI


class GUIPlugin(BasePlugin):
    namespace = "game"

    def __init__(self):
        super().__init__()
        self.gui = GameGUI()

    def _register_events(self):
        self._sio.on("game_start", self.on_game_start)
        self._sio.on("game_update", self.on_game_update)
        self._sio.on("game_over", self.on_game_over)

    async def on_game_start(self, _, __):
        self.gui.set_data(self._namespace_data["data"])

    async def on_game_update(self, _, __):
        self.gui.update()

    async def on_game_over(self, _, __):
        await asyncio.sleep(5)
        self.gui.reset()
