import asyncio
import logging
import pickle
from collections import deque
from pathlib import Path
from typing import Any

from generals_bot.base import BasePlugin

logger = logging.getLogger(__name__)


class PlaybackPlugin(BasePlugin):
    namespace = "game"

    def __init__(self, record_filepath: Path | str) -> None:
        super().__init__()

        self.record_filepath: Path = (
            Path(record_filepath)
            if isinstance(record_filepath, str)
            else record_filepath
        )

        assert self.record_filepath.exists(), f"{self.record_filepath} does not exist"
        assert self.record_filepath.is_file(), f"{self.record_filepath} is not a file"

    def _register_events(self) -> None:
        async def _nothing(*args, **kwargs):
            return None

        self._sio.emit = _nothing
        logger.info("Disabled emitting events for playback")

        asyncio.ensure_future(self.play_record())

    async def _mock_event(self, event: str, data: Any, namespace: str = "/") -> None:
        await self._sio._trigger_event(event, namespace, data, None)

    async def play_record(self) -> None:
        with self.record_filepath.open("rb") as f:
            data: deque = pickle.load(f)

        initial_data = data.popleft()
        await self._mock_event("game_start", initial_data)

        for update in data:
            await self._mock_event("game_update", update)
            await asyncio.sleep(1)

        await self._mock_event("game_over", None)
