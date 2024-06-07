from dataclasses import dataclass
from enum import IntEnum, auto, IntFlag
from functools import cached_property
from typing import NamedTuple

from .dto import ScoreData

type Army = int


class Terrain(IntFlag, boundary=True):
    EMPTY = -1
    MOUNTAIN = -2
    FOG = -3
    OBSTACLE = -4

    @property
    def is_player(self) -> bool:
        return self >= 0


class MapBlock(NamedTuple):
    index: int
    x: int
    y: int
    army: Army
    terrain: Terrain
    is_city: bool
    is_general: bool


class PlayerColor(IntEnum):
    RED = 0
    BLUE = auto()
    GREEN = auto()
    CYAN = auto()
    ORANGE = auto()
    PINK = auto()
    PURPLE = auto()
    DEEP_RED = auto()
    YELLOW = auto()
    BROWN_YELLOW = auto()
    DEEP_BLUE = auto()
    INDIGO = auto()


@dataclass
class Player:
    username: str
    team: int
    _color: int
    score: ScoreData | None = None

    @cached_property
    def color(self) -> PlayerColor:
        return PlayerColor(self._color)
