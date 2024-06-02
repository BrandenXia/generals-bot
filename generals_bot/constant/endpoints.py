from types import MappingProxyType
from typing import Literal

from generals_bot.utils import URL

type ServerType = Literal["human", "bot"]

type ProtocolType = Literal["ws", "https"]

URLS: dict[ServerType, dict[ProtocolType, URL]] = MappingProxyType(
    {
        "human": {
            "ws": URL(netloc="ws.generals.io"),
            "https": URL(netloc="generals.io"),
        },
        "bot": {
            "ws": URL(netloc="botws.generals.io"),
            "https": URL(netloc="bot.generals.io"),
        },
    }
)
