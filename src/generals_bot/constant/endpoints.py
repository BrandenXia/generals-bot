from collections.abc import Mapping
from types import MappingProxyType

from generals_bot.types.endpoints import ServerType, ProtocolType
from generals_bot.utils import URL

# Mapping of server type to protocol type to general.io URL
URLS: Mapping[ServerType, Mapping[ProtocolType, URL]] = MappingProxyType(
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
