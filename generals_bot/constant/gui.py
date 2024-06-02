from enum import IntEnum, auto, IntFlag

BG_COLOR = (34, 34, 34)
TEXT_COLOR = (255, 255, 255)


class Terrain(IntFlag, boundary=True):
    EMPTY = -1
    MOUNTAIN = -2
    FOG = -3
    OBSTACLE = -4

    @property
    def is_player(self) -> bool:
        return self >= 0

    @property
    def color(self) -> tuple[int, int, int]:
        match self:
            case Terrain.EMPTY:
                return 220, 220, 220
            case Terrain.MOUNTAIN:
                return 187, 187, 187
            case Terrain.FOG | Terrain.OBSTACLE:
                return 128, 128, 128
            case _:
                return PLAYER_COLOR_RGB[self]


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

    @property
    def rgb(self) -> tuple[int, int, int]:
        return PLAYER_COLOR_RGB[self]


PLAYER_COLOR_RGB = {
    PlayerColor.RED: (255, 0, 0),
    PlayerColor.BLUE: (67, 99, 216),
    PlayerColor.GREEN: (0, 128, 0),
    PlayerColor.CYAN: (0, 128, 128),
    PlayerColor.ORANGE: (245, 130, 49),
    PlayerColor.PINK: (240, 50, 230),
    PlayerColor.PURPLE: (128, 0, 128),
    PlayerColor.DEEP_RED: (128, 0, 0),
    PlayerColor.YELLOW: (176, 159, 48),
    PlayerColor.BROWN_YELLOW: (154, 99, 36),
    PlayerColor.DEEP_BLUE: (0, 0, 255),
    PlayerColor.INDIGO: (72, 61, 139),
}
