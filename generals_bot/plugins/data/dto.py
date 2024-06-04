from typing import TypedDict, Any, Literal

type GameType = Literal["ffa", "1v1", "custom"]


class InitialData(TypedDict):
    playerIndex: int
    playerColors: list[int]
    replay_id: str
    chat_room: str
    usernames: list[str]
    teams: list[int]
    game_type: GameType
    swamps: list[Any]
    lights: list[Any]
    options: dict[str, Any]


class ScoreData(TypedDict):
    total: int
    tiles: int
    i: int
    color: int
    dead: bool


class UpdateData(TypedDict):
    scores: list[ScoreData]
    turn: int
    stars: list[int]
    attackIndex: int
    generals: list[int]
    map_diff: list[int]
    cities_diff: list[int]
