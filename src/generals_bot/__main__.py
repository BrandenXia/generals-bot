import asyncio
import logging
import os

from dotenv import load_dotenv

from generals_bot import GeneralsClient
from generals_bot.plugins import (
    GeneralsPlugin,
    PlaybackPlugin,
    GlobalListener,
    DataListener,
    GUIPlugin,
    PlayerPlugin,
    PersistentPlugin,
)

load_dotenv()

logger = logging.getLogger(__name__)


async def _main():
    async with GeneralsClient(
        server="bot",
        plugins=[
            GeneralsPlugin(
                user_id=os.getenv("USER_ID"),
                username=os.getenv("USERNAME"),
            ),
            PlaybackPlugin(),
            GlobalListener(),
            DataListener(),
            PersistentPlugin(),
            GUIPlugin(),
            PlayerPlugin(),
        ],
        debug=True,
    ) as client:
        await client.join_private("test1", force_start=True)


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    main()
