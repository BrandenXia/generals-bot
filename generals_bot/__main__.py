import asyncio
import logging
import os

from dotenv import load_dotenv

from generals_bot import GeneralsClient
from generals_bot.plugins import (
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
        user_id=os.getenv("USER_ID"),
        username=os.getenv("USERNAME"),
        server="bot",
        plugins=[
            GlobalListener(),
            DataListener(),
            PersistentPlugin(),
            GUIPlugin(),
            PlayerPlugin(),
        ],
        debug=True,
    ) as client:
        await client.join_private("test", force_start=True)


def main():
    try:
        asyncio.run(_main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Interrupted, exiting...")


if __name__ == "__main__":
    main()
