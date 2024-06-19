import asyncio
import pickle
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from generals_bot.base import BasePlugin


class PlaybackPlugin(BasePlugin):
    """Replay a game of generals.io from a record file"""

    @property
    def methods(self) -> tuple[str, ...]:
        return ("play_record",)

    @contextmanager
    def __disable_emit(self) -> Generator[None, None, None]:
        async def _nothing(*_: Any, **__: Any) -> None:
            return None

        tmp, self._sio.emit = self._sio.emit, _nothing

        try:
            yield
        finally:
            self._sio.emit = tmp

    async def __mock_event(self, event: str, data: Any, namespace: str = "/") -> None:
        await self._sio._trigger_event(event, namespace, data, None)

    async def play_record(self, record_path: Path | str) -> None:
        """
        Play a game from a record file
        :param record_path: path to the record file, can be a string or a Path object
        """
        record_filepath: Path = (
            Path(record_path) if isinstance(record_path, str) else record_path
        )

        assert record_filepath.exists(), f"{record_filepath} does not exist"
        assert record_filepath.is_file(), f"{record_filepath} is not a file"

        with record_filepath.open("rb") as f:
            data = pickle.load(f)

        with self.__disable_emit():
            initial_data = data.popleft()
            await self.__mock_event("game_start", initial_data)

            for update in data:
                await self.__mock_event("game_update", update)
                await asyncio.sleep(1)

            await self.__mock_event("game_over", None)
