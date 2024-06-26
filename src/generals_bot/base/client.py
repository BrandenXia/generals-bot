import asyncio
import logging

from socketio import AsyncClient

from generals_bot.constant.endpoints import URLS
from generals_bot.socketio import MultiHandlerAsyncClient
from generals_bot.types.endpoints import ServerType

logger = logging.getLogger(__name__)


class BaseClient:
    """Base client for generals.io"""

    def __init__(
        self,
        server: ServerType,
        sio: AsyncClient | None = None,
    ) -> None:
        """
        :param server: "human" or "bot", currently only "bot" is supported due to generals.io restrictions
        :param sio: socket.io client, defaults to MultiHandlerAsyncClient
        """
        logger.debug(f"Server: {repr(server)}")

        self._sio = sio or MultiHandlerAsyncClient()

        self.url = URLS[server]

        logger.info(f"{repr(self.__class__.__name__)} initialized")

    async def connect(self) -> None:
        """Connect to the server"""
        logger.info(f'Connecting to server {repr(self.url["ws"].build())}')
        await self._sio.connect(self.url["ws"].build())

    async def disconnect(self) -> None:
        await self._sio.disconnect()

    async def wait(self) -> None:
        try:
            await self._sio.wait()
        except (KeyboardInterrupt, asyncio.CancelledError):
            logger.info("KeyboardInterrupt, disconnecting...")
            await self.disconnect()
