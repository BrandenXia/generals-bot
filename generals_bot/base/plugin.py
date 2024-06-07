import logging
from abc import ABC, abstractmethod
from typing import final

from socketio import AsyncClient

logger = logging.getLogger(__name__)


class BasePlugin(ABC):
    """Base class for all plugins. All plugins should inherit from this class"""

    @property
    @abstractmethod
    def namespace(self):
        """Namespace of the plugin, for sharing data between plugins"""
        pass

    def __init__(self) -> None:
        """Initialized plugin, can be overridden to add custom settings for the plugin"""
        self._sio: AsyncClient | None = None
        self._namespace_data: dict | None = None

        logger.info(f"Plugin {self.__class__.__name__} initialized")

    @final
    def connect(self, sio: AsyncClient, namespace_data: dict) -> None:
        """
        Connects the plugin to the socketio client and namespace data, should not be overridden
        :param sio: socket.io client
        :param namespace_data: data shared between plugins
        """
        self._sio = sio
        self._namespace_data = namespace_data

        self._register_events()
        logger.info(f"Registered events for {self.__class__.__name__}")

    @abstractmethod
    def _register_events(self) -> None:
        """Registers events for the plugin, overridden to add custom after connected to the socketio client"""
        pass
