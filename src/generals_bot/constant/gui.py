from generals_bot.types.map import PlayerColor, Terrain

BG_COLOR = (34, 34, 34)
TEXT_COLOR = (255, 255, 255)

TERRAIN_COLOR_RGB = {
    Terrain.EMPTY: (220, 220, 220),
    Terrain.MOUNTAIN: (187, 187, 187),
    Terrain.FOG: (128, 128, 128),
    Terrain.OBSTACLE: (128, 128, 128),
}

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
