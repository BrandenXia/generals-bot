import logging

from generals_bot.base import BasePlugin

logger = logging.getLogger(__name__)


class GlobalListener(BasePlugin):
    """Global listener plugin that listens to all events"""

    namespace = "global"

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
