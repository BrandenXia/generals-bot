from collections import defaultdict

from socketio import AsyncClient

from .plugin import BasePlugin


class Namespace:
    """Namespace class to manage plugins and share data between them"""

    def __init__(
        self, sio: AsyncClient, plugins: list[BasePlugin] | None = None
    ) -> None:
        """
        :param sio: socket.io client
        :param plugins: list of plugins to register, can be added later
        """
        self._sio = sio
        self._plugins = plugins or []
        self._data = defaultdict(lambda: None)

    def add_plugin(self, plugin: BasePlugin) -> None:
        """
        Add a plugin to the namespace, should be called before registering
        :param plugin: plugin to add
        """
        assert isinstance(plugin, BasePlugin)
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
        [self._register_plugin(plugin) for plugin in self._plugins]
