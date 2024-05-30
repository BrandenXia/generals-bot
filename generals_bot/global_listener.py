from socketio import AsyncClient

from generals_bot.base import BaseListener
from generals_bot.logger import logger


class GlobalListener(BaseListener):
    _sio: AsyncClient

    def __init__(self) -> None:
        logger.info("GlobalListener initialized")
        self._sio.on("connect", self.on_connect)
        self._sio.on("connect_error", self.on_connect_error)
        self._sio.on("disconnect", self.on_disconnect)
        self._sio.on("*", self.on_message)

    @staticmethod
    def on_connect():
        logger.info("Connected to server")

    @staticmethod
    def on_connect_error(data):
        logger.error(f"Error: {repr(data)}")

    @staticmethod
    def on_disconnect():
        logger.info("Disconnected from server")

    @staticmethod
    async def on_message(event: str, data=None, msg=None):
        logger.debug(
            f"Event: {repr(event)} | Data: {repr(data)} | Message: {repr(msg)}"
        )
