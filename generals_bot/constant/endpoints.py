from typing import Literal

from generals_bot.utils import URL

URLS: dict[Literal["human", "bot"], dict[Literal["ws", "https"], URL]] = {
    "human": {"ws": URL(netloc="ws.generals.io"), "https": URL(netloc="generals.io")},
    "bot": {
        "ws": URL(netloc="botws.generals.io"),
        "https": URL(netloc="bot.generals.io"),
    },
}
