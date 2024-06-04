from collections import defaultdict

from socketio import AsyncClient

from .plugin import BasePlugin


class Namespace:
    def __init__(self, sio: AsyncClient, plugins: list[BasePlugin] | None = None):
        self._sio = sio
        self._plugins = plugins or []
        self._data = defaultdict(lambda: None)

    def add_plugin(self, plugin: BasePlugin):
        assert isinstance(plugin, BasePlugin)
        self._plugins.append(plugin)

    def _register_plugin(self, plugin: BasePlugin):
        assert isinstance(plugin, BasePlugin)
        plugin.connect(self._sio, self._data)

    def register_plugins(self):
        [self._register_plugin(plugin) for plugin in self._plugins]
