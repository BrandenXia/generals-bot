import logging
from collections.abc import Sequence
from functools import cached_property
from operator import attrgetter

from .dto import InitialData, UpdateData
from .types import (
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

        self._turn: int = 0
        self.map = Map()

        logger.debug(f"GameData: {repr(self)}")

        logger.info(f'Game initialized"')

    @property
    def turn(self) -> int:
        return self._turn

    def update(self, data: UpdateData):
        self._turn = data["turn"]
        self.map.update(data)

        logger.debug(f"GameData: {repr(self)}")

    def __repr__(self):
        return f"GameData(turn={self.turn}, players={self.players}, map={self.map})"


def _get_players(initial_data: InitialData) -> Sequence[Player]:
    return [
        Player(*player_data)
        for player_data in zip(
            initial_data["usernames"],
            initial_data["teams"],
            initial_data["playerColors"],
        )
    ]


class Map:
    def __init__(self):
        self._generals: list[int] = []
        self._cities: list[int] = []
        self._map: list[int] = []

    @cached_property
    def armies(self) -> Sequence[Army]:
        return self._map[2 : 2 + self.size] if self._map else []

    @cached_property
    def terrain(self) -> Sequence[Terrain]:
        terrain = self._map[2 + self.size : 2 + 2 * self.size] if self._map else []
        return [Terrain(t) for t in terrain]

    @cached_property
    def width(self) -> int:
        """Return the number of columns in the map"""
        return self._map[0] if self._map else 0

    @cached_property
    def height(self) -> int:
        """Return the number of rows in the map"""
        return self._map[1] if self._map else 0

    @cached_property
    def size(self) -> int:
        return self.width * self.height

    def __iter__(self):
        return (
            MapBlock(
                i,
                *divmod(i, self.width)[::-1],
                army=self.armies[i],
                terrain=self.terrain[i],
                is_city=i in self._cities,
                is_general=i in self._generals,
            )
            for i in range(self.size)
        )

    def __getitem__(
        self, item: tuple[int | slice, int | slice, tuple[str, ...]]
    ) -> Sequence[MapBlock]:
        fields = item[2] if len(item) > 2 else MapBlock._fields

        x = item[0] if isinstance(item[0], slice) else slice(item[0], item[0] + 1)
        y = item[1] if len(item) > 1 else slice(0, self.height)
        y = y if isinstance(y, slice) else slice(y, y + 1)

        if x == slice(None):
            x = slice(0, self.width)
        if y == slice(None):
            y = slice(0, self.height)

        if x.step or y.step:
            raise ValueError("Only single index access is supported")

        return [
            attrgetter(*fields)(block)
            for block in self
            if x.start <= block.x < x.stop and y.start <= block.y < y.stop
        ]

    def get_around(self, x: int, y: int, radius: int) -> Sequence[MapBlock]:
        return [
            block for block in self if abs(block.x - x) + abs(block.y - y) <= radius
        ]

    def update(self, data: UpdateData):
        self._update_generals(data["generals"])
        self._map = self._patch(self._map, data["map_diff"])
        self._cities = self._patch(self._cities, data["cities_diff"])
        self._clear_cache()

    def _update_generals(self, generals: Sequence[int]):
        self._generals = (
            [old if new == -1 else new for old, new in zip(self._generals, generals)]
            if self._generals
            else generals
        )

    def _clear_cache(self):
        for name in dir(type(self)):
            if isinstance(getattr(type(self), name), cached_property):
                vars(self).pop(name, None)

    @staticmethod
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

    def __repr__(self):
        return f"Map(width={self.width}, height={self.height}, generals={self._generals}, cities={self._cities})"
