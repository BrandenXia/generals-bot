import asyncio
import os

from dotenv import load_dotenv

from generals_bot import GeneralsClient

load_dotenv()


def main():
    client = GeneralsClient(
        user_id=os.getenv("USER_ID"),
        username=os.getenv("USERNAME"),
        server="bot",
        debug=True,
    )

    client_task = asyncio.ensure_future(client.run())
    try:
        asyncio.get_event_loop().run_forever()
    finally:
        client_task.cancel()


if __name__ == "__main__":
    main()
