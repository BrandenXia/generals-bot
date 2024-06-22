from collections import defaultdict
from collections.abc import Callable
from typing import Any

from socketio import AsyncClient

from .plugin import BasePlugin


class Namespace:
    """Namespace class to manage plugins and share data between them"""

    def __init__(
        self, bind: Callable[[str, Callable[..., Any]], None], sio: AsyncClient
    ) -> None:
        """
        :param bind: function to bind a method to the parent client
        :param sio: socket.io client
        """
        self._bind = bind
        self._sio = sio
        self._plugins: list[BasePlugin] = []
        self._data: dict[str, Any] = defaultdict()

    def load_plugin(self, plugin: BasePlugin) -> None:
        """
        Load a plugin into the namespace
        :param plugin: plugin to load
        """
        assert isinstance(
            plugin, BasePlugin
        ), "Plugin must be an instance of BasePlugin"

        for name in plugin.methods:
            method = getattr(plugin, name)
            self._bind(name, method)

        plugin.connect(self._sio, self._data)
        self._plugins.append(plugin)
