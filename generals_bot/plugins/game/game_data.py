import logging
from collections.abc import Sequence
from typing import Any, Generator

from generals_bot.plugins.game.dto import InitialData, UpdateData
from generals_bot.plugins.game.types import (
    Terrain,
    Player,
    MapBlock,
    Army,
)

logger = logging.getLogger(__name__)


class GameData:
    def __init__(self, initial_data: InitialData):
        logger.debug(f"InitialData: {repr(initial_data)}")

        self.game_type = initial_data["game_type"]
        self.replay_id: str = initial_data["replay_id"]
        self.player_index: int = initial_data["playerIndex"]
        self.players: Sequence[Player] = _get_players(initial_data)

        self._generals: list[int] = []
        self._cities: list[int] = []
        self._map: list[int] = []

        logger.debug(f"GameData: {repr(self)}")

        logger.info(f'Game initialized"')

    @property
    def width(self) -> int:
        """Return the number of columns in the map"""
        return self._map[0] if self._map else 0

    @property
    def height(self) -> int:
        """Return the number of rows in the map"""
        return self._map[1] if self._map else 0

    @property
    def size(self) -> int:
        return self.width * self.height

    @property
    def generals(self) -> Sequence[int]:
        return self._generals

    @property
    def cities(self) -> Sequence[int]:
        return self._cities

    @property
    def armies(self) -> Sequence[Army]:
        return self._map[2 : 2 + self.size] if self._map else []

    @property
    def terrain(self) -> Sequence[Terrain]:
        terrain = self._map[2 + self.size : 2 + 2 * self.size] if self._map else []
        return [Terrain(t) for t in terrain]

    @property
    def map(self) -> Generator[MapBlock, Any, None]:
        return (
            MapBlock(
                army=self.armies[i],
                terrain=self.terrain[i],
                is_city=i in self._cities,
                is_general=i in self._generals,
            )
            for i in range(self.size)
        )

    def update_generals(self, generals: Sequence[int]):
        self._generals = [
            old if new == -1 else new for old, new in zip(self._generals, generals)
        ]

    def update(self, data: UpdateData):
        self.update_generals(data["generals"])
        self._map = _patch(self._map, data["map_diff"])
        self._cities = _patch(self._cities, data["cities_diff"])

        logger.debug(f"GameData: {repr(self)}")

    def __repr__(self):
        return (
            f"GameData(generals={repr(self._generals)}, width={repr(self.width)}, height={repr(self.height)}, "
            f"size={repr(self.size)}, players={repr(self.players)}, cities={repr(self._cities)})"
        )


def _patch(old: Sequence[int], diff: Sequence[int]) -> Sequence[int]:
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


def _get_players(initial_data: InitialData) -> Sequence[Player]:
    return [
        Player(*player_data)
        for player_data in zip(
            initial_data["usernames"],
            initial_data["teams"],
            initial_data["playerColors"],
        )
    ]
