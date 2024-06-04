import asyncio
import os

from dotenv import load_dotenv

from generals_bot import GeneralsClient
from generals_bot.plugins import GlobalListener, DataListener, GUIPlugin

load_dotenv()


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = GeneralsClient(
        user_id=os.getenv("USER_ID"),
        username=os.getenv("USERNAME"),
        server="bot",
        plugins=[GlobalListener(), DataListener(), GUIPlugin()],
        debug=True,
    )

    client_task = asyncio.ensure_future(client.run())

    try:
        loop.run_until_complete(client_task)
    finally:
        client_task.cancel()


if __name__ == "__main__":
    main()
