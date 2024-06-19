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

    def add_plugin(self, plugin: BasePlugin) -> None:
        """
        Add a plugin to the namespace, should be called before registering
        :param plugin: plugin to add
        """
        assert isinstance(plugin, BasePlugin)

        for name in plugin.methods:
            method = getattr(plugin, name)
            self._bind(name, method)

        self._plugins.append(plugin)

    def _register_plugin(self, plugin: BasePlugin) -> None:
        """
        Connect a plugin to the namespace
        :param plugin: plugin to connect
        """
        assert isinstance(plugin, BasePlugin)
        plugin.connect(self._sio, self._data)

    def register_plugins(self) -> None:
        """Register all plugins in the namespace"""
        for plugin in self._plugins:
            self._register_plugin(plugin)
