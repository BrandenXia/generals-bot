import asyncio
import os
from typing import cast, Literal

from dotenv import load_dotenv

from generals_bot import GeneralsClient

load_dotenv()


async def main():
    client = GeneralsClient(
        user_id=os.getenv("USER_ID"),
        username=os.getenv("USERNAME"),
        server=cast(Literal["human", "bot"], os.getenv("SERVER")),
        debug=True
    )
    await client.connect()
    await client.join_private("test", force_start=True),
    await client.wait()

if __name__ == "__main__":
    asyncio.run(main())
