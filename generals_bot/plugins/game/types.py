from dataclasses import dataclass
from functools import cached_property
from typing import NamedTuple

from generals_bot.constant.gui import PlayerColor, Terrain
from generals_bot.plugins.game.dto import ScoreData

type Army = int


class MapBlock(NamedTuple):
    x: int
    y: int
    army: Army
    terrain: Terrain
    is_city: bool
    is_general: bool


@dataclass
class Player:
    username: str
    team: int
    _color: int
    score: ScoreData | None = None

    @cached_property
    def color(self) -> PlayerColor:
        return PlayerColor(self._color)
