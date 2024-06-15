import logging

from socketio import AsyncClient

from generals_bot.constant import endpoints
from generals_bot.constant.endpoints import ServerType
from generals_bot.socketio import MultiHandlerAsyncClient

logger = logging.getLogger(__name__)


class BaseClient:
    """Base client for generals.io"""

    def __init__(
        self,
        user_id: str,
        username: str,
        server: ServerType,
        sio: AsyncClient | None = None,
    ) -> None:
        """
        :param user_id: user ID, should be unique, consistent, and secret
        :param username: username to display
        :param server: "human" or "bot", currently only "bot" is supported due to generals.io restrictions
        :param sio: socket.io client, defaults to MultiHandlerAsyncClient
        """
        logger.debug(f"Username: {repr(username)} | Server: {repr(server)}")

        self._sio = sio or MultiHandlerAsyncClient()

        self.user_id = user_id
        self.username = username
        self.url = endpoints.URLS[server]

        logger.info(f"{repr(self.__class__.__name__)} initialized")

    async def connect(self) -> None:
        """Connect to the server"""
        logger.info(f'Connecting to server {repr(self.url["ws"].build())}')
        await self._sio.connect(self.url["ws"].build())

    async def disconnect(self) -> None:
        await self._sio.disconnect()
