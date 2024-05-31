import logging

from generals_bot.game.types import InitialData, UpdateData

logger = logging.getLogger(__name__)


class GameData:
    def __init__(self, initial_data: InitialData):
        logger.info(f'Game initialized"')

        self.game_type = initial_data["game_type"]
        self.replay_id: str = initial_data["replay_id"]
        self.player_index: int = initial_data["playerIndex"]

        self.generals: list[int] = []
        self._cities: list[int] = []
        self._map: list[int] = []

        logger.debug(f"GameData: {repr(self)}")

    @property
    def width(self) -> int:
        return self._map[0] if self._map else 0

    @property
    def height(self) -> int:
        return self._map[1] if self._map else 0

    @property
    def size(self) -> int:
        return self.width * self.height

    @property
    def armies(self) -> list[int]:
        return self._map[2 : 2 + self.size] if self._map else []

    @property
    def terrain(self) -> list[int]:
        return self._map[2 + self.size : 2 + 2 * self.size] if self._map else []

    @staticmethod
    def _patch(old: list[int], diff: list[int]) -> list[int]:
        new: list[int] = []
        i = 0
        while i < len(diff):
            if diff[i]:
                new.extend(old[len(new) : len(new) + diff[i]])
            i += 1

            if i < len(diff) and diff[i]:
                new.extend(diff[i + 1 : i + 1 + diff[i]])
                i += diff[i]
            i += 1

        return new

    def update(self, data: UpdateData):
        logger.info("Game updated")

        self.generals = data["generals"]
        self._cities = self._patch(self._cities, data["cities_diff"])
        self._map = self._patch(self._map, data["map_diff"])

        logger.debug(f"GameData: {repr(self)}")

    def __repr__(self):
        return (
            f"GameData(generals={repr(self.generals)}, width={repr(self.width)}, height={repr(self.height)}, "
            f"size={repr(self.size)}, armies={repr(self.armies)}, terrain={repr(self.terrain)}), "
            f"cities={repr(self._cities)})"
        )
