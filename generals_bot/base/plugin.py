import logging
from abc import ABC, abstractmethod

from socketio import AsyncClient

logger = logging.getLogger(__name__)


class BasePlugin(ABC):
    def __init__(self):
        self._sio: AsyncClient | None = None

        logger.info(f"Plugin {self.__class__.__name__} initialized")

    def set_sio(self, sio: AsyncClient):
        self._sio = sio

        self._register_events()
        logger.info(f"Registered events for {self.__class__.__name__}")

    @abstractmethod
    def _register_events(self):
        pass
