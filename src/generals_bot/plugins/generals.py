import logging
from typing import Any

from generals_bot.base import BasePlugin

logger = logging.getLogger(__name__)


class GeneralsPlugin(BasePlugin):
    """Basic operations for generals.io"""

    @property
    def methods(self) -> tuple[str, ...]:
        return "set_username", "join_private"

    def __init__(self, user_id: str, username: str) -> None:
        """
        :param user_id: generals.io user ID
        :param username: generals.io username
        """
        self.user_id = user_id
        self.username = username

        super().__init__()

    async def set_username(self) -> None:
        """Set username for the client, should only be called once forever for each user ID"""
        await self._sio.emit("set_username", (self.user_id, self.username))
        logger.info(
            f"Set username to {repr(self.username)} with user ID {repr(self.user_id)}"
        )

    async def join_private(
        self, custom_game_id: str, force_start: bool = False
    ) -> None:
        """
        Join a private game
        :param custom_game_id: can be a combination of letters, numbers, and underscores
        :param force_start: whether to force start the game
        """
        await self._sio.emit("join_private", (custom_game_id, self.user_id))
        logger.info(f"Joined private game at game ID {repr(custom_game_id)}")

        if force_start:

            @self._sio.on("queue_update")  # type: ignore
            async def on_queue_update(_: Any) -> None:
                await self.set_force_start(custom_game_id)
                del self._sio.handlers["/"]["queue_update"]

    async def set_force_start(self, custom_game_id: str) -> None:
        """Force start a game"""
        await self._sio.emit("set_force_start", (custom_game_id, self.user_id))
        logger.info(f"Force started private game with ID {repr(custom_game_id)}")
