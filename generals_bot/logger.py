import logging

from rich.logging import RichHandler

logger = logging.getLogger("generals_bot")
logger.handlers = [RichHandler()]
logger.setLevel(logging.DEBUG)

logger.info("Logger initialized")
