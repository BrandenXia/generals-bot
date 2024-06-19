import logging
from abc import ABC, abstractmethod
from typing import final, Any

from socketio import AsyncClient

logger = logging.getLogger(__name__)


class BasePlugin(ABC):
    """Base class for all plugins. Method names starting with 'on_' are registered as events"""

    @property
    @abstractmethod
    def namespace(self) -> str:
        """Namespace of the plugin, for sharing data between plugins"""
        pass

    def __init__(self) -> None:
        """Initialized plugin, can be overridden to add custom settings for the plugin"""
        self._sio: AsyncClient | None = None
        self._namespace_data: dict[str, Any] | None = None

        logger.info(f"Plugin {repr(self.__class__.__name__)} initialized")

    @final
    def connect(self, sio: AsyncClient, namespace_data: dict[str, Any]) -> None:
        """
        Connects the plugin to the socketio client and namespace data, should not be overridden
        :param sio: socket.io client
        :param namespace_data: data shared between plugins
        """
        self._sio = sio
        self._namespace_data = namespace_data

        self._plugin_initialize()
        logger.info(f"Initialized plugin {repr(self.__class__.__name__)}")

        self._register_events()

    @final
    def _register_events(self) -> None:
        """Register events for the plugin, called after `_plugin_initialize` method, should not be overridden"""
        assert self._sio is not None, "SocketIO client not initialized"

        for method_name in dir(self):
            if method_name.startswith("on_"):
                event_name = method_name[3:]
                self._sio.on(event_name, getattr(self, method_name))
                logger.info(
                    f"Registered event '{event_name}' for {repr(self.__class__.__name__)}"
                )

    def _plugin_initialize(self) -> None:
        """Initialize plugin, called after connecting to the socketio client"""
        pass
