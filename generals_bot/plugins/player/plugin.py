from typing import cast

from generals_bot.base import BasePlugin
from generals_bot.plugins.data import GameData
from generals_bot.utils import timeit


class PlayerPlugin(BasePlugin):
    """Player plugin for controlling the bot"""

    namespace = "game"

    def _register_events(self):
        self._sio.on("game_update", self.on_game_update)

    @timeit
    async def on_game_update(self, _, __):
        # TODO: Rewrite this to simplify the logic
        data = cast(GameData, self._namespace_data["data"])

        weights = [[0 for _ in range(data.map.width)] for _ in range(data.map.height)]

        for block in data.map:
            weight = 1

            if block.terrain == data.player_index and block.army > 1:
                army = block.army
            else:
                continue

            weight *= army / 2

            if block.is_city or block.is_general:
                weight *= 2

            weights[block.y][block.x] = weight

        blocks = []
        for y, row in enumerate(weights):
            for x, weight in enumerate(row):
                blocks.append((x, y, weight))

        blocks.sort(key=lambda x: x[2], reverse=True)
        blocks = blocks[:10]

        moves = []
        for block in blocks:
            around = data.map.get_around(block[0], block[1], 1)
            for a in around:
                weight = block[2] + (
                    a.army / 2 if a.terrain != data.player_index else -a.army / 2
                )
                src = data.map[block[0], block[1]]
                dst = a.index
                moves.append((src, dst, weight))

        moves.sort(key=lambda x: x[2], reverse=True)
        best = moves[0]

        await self._sio.emit("attack", (best[0], best[1], False))
