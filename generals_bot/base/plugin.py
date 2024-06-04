import logging
from abc import ABC, abstractmethod

from socketio import AsyncClient

logger = logging.getLogger(__name__)


class BasePlugin(ABC):
    @property
    @abstractmethod
    def namespace(self):
        pass

    def __init__(self):
        self._sio: AsyncClient | None = None
        self._namespace_data: dict | None = None

        logger.info(f"Plugin {self.__class__.__name__} initialized")

    def connect(self, sio: AsyncClient, namespace_data: dict):
        self._sio = sio
        self._namespace_data = namespace_data

        self._register_events()
        logger.info(f"Registered events for {self.__class__.__name__}")

    @abstractmethod
    def _register_events(self):
        pass
