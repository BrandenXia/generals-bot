import asyncio
import logging

from socketio import AsyncClient

from generals_bot.constant import endpoints
from generals_bot.constant.endpoints import ServerType
from generals_bot.socketio import MultiHandlerAsyncClient

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(
        self,
        user_id: str,
        username: str,
        server: ServerType,
        sio: AsyncClient | None = None,
    ):
        logger.debug(f"Username: {repr(username)} | Server: {repr(server)}")

        self._sio = sio or MultiHandlerAsyncClient()

        self.user_id = user_id
        self.username = username
        self.url = endpoints.URLS[server]

        logger.info(f"{self.__class__.__name__} initialized")

    async def set_username(self):
        await self._sio.emit("set_username", (self.user_id, self.username))
        logger.info(f'Set username to "{self.username}" with user ID "{self.user_id}"')

    async def connect(self, set_username: bool = False):
        logger.info(f'Connecting to server "{self.url["ws"].build()}"')
        await self._sio.connect(self.url["ws"].build())

        if set_username:
            await self.set_username()

    async def wait(self):
        try:
            logger.info("Waiting for events")
            await self._sio.wait()
        except (asyncio.CancelledError, KeyboardInterrupt):
            logger.info("Received KeyboardInterrupt, disconnect")
            await self._sio.disconnect()

    async def join_private(self, custom_game_id: str, force_start: bool = False):
        await self._sio.emit("join_private", (custom_game_id, self.user_id))
        logger.info(
            f'Joined private game at "{self.url["https"].url(f"/games/{custom_game_id}").build()}"'
        )

        if force_start:

            @self._sio.on("queue_update")
            async def on_queue_update(_):
                await self.set_force_start(custom_game_id)
                del self._sio.handlers["/"]["queue_update"]

    async def set_force_start(self, custom_game_id: str):
        await self._sio.emit("set_force_start", (custom_game_id, self.user_id))
        logger.info(f'Force started private game with ID "{custom_game_id}"')
