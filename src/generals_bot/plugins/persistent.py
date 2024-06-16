import logging
import pickle
from collections import deque
from datetime import datetime
from pathlib import Path

from generals_bot.base import BasePlugin

logger = logging.getLogger(__name__)


class PersistentPlugin(BasePlugin):
    """Plugin that persists data of each game"""

    namespace = "game"

    def __init__(self, persist_dir: Path | str = Path.cwd() / "records") -> None:
        super().__init__()

        self.persist_dir: Path = (
            Path(persist_dir) if isinstance(persist_dir, str) else persist_dir
        )

        if not self.persist_dir.exists():
            self.persist_dir.mkdir(parents=True)

        assert self.persist_dir.is_dir(), f"{self.persist_dir} is not a directory"

        self.current_data: deque | None = None

    async def on_game_start(self, data, __) -> None:
        self.current_data = deque()
        self.current_data.append(data)

        logger.info("Persistent data initialized")

    async def on_game_update(self, data, __) -> None:
        self.current_data.append(data)

        logger.info("Persistent data updated")

    async def on_game_over(self, _, __) -> None:
        if self.current_data is None:
            return

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        game_id = self.current_data[0]["replay_id"]
        filename = f"{date}_{game_id}"
        file = (self.persist_dir / filename).with_suffix(".pickle")

        with file.open("wb") as f:
            pickle.dump(self.current_data, f)

        logger.info(f"Persistent data saved to {file}")
