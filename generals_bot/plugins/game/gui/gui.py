import asyncio
import logging
from pathlib import Path

from generals_bot.plugins.game import GameData
from generals_bot.plugins.game.gui.silent_pygame import silent_pygame
from generals_bot.plugins.game.types import Terrain

pygame = silent_pygame()

logger = logging.getLogger(__name__)


class GameGUI:
    def __init__(self):
        logger.info("GameGUI initialized")

        self._data: GameData | None = None

        pygame.init()
        self.win = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Generals.io Bot")

        assets = Path(__file__).parent / "assets"

        self.font = pygame.font.Font(assets / "Quicksand-Medium.ttf", 20)

        self.mountain = pygame.image.load(assets / "mountain.png")
        self.obstacle = pygame.image.load(assets / "obstacle.png")
        self.crown = pygame.image.load(assets / "crown.png")
        self.city = pygame.image.load(assets / "city.png")

        self.border = 2

        self._init_screen()

        asyncio.ensure_future(self.pygame_event_loop())

    def _init_screen(self):
        self.win.fill((34, 34, 34))
        self.win.blit(
            self.font.render("Generals.io Bot", True, (255, 255, 255)), (10, 10)
        )
        pygame.display.flip()

    def reset(self):
        self._init_screen()
        self._data = None

    def set_data(self, data: GameData):
        self._data = data

    @staticmethod
    async def pygame_event_loop():
        logger.info("Starting pygame event loop")
        while True:
            await asyncio.sleep(0)
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break
        pygame.quit()
        logger.info("Stopped pygame event loop")

    def render_terrain(self, start_x: int, start_y: int, unit: int, terrain: Terrain):
        color: tuple[int, int, int]
        match terrain:
            case Terrain.EMPTY:
                color = (220, 220, 220)
            case Terrain.MOUNTAIN:
                color = (187, 187, 187)
            case Terrain.FOG | Terrain.OBSTACLE:
                color = (128, 128, 128)
            case _:
                color = self._data.players[terrain].color.rgb
        pygame.draw.rect(self.win, color, (start_x, start_y, unit, unit))

        img: pygame.Surface

        match terrain:
            case Terrain.MOUNTAIN:
                img = pygame.transform.scale(self.mountain, (unit, unit))
            case Terrain.OBSTACLE:
                img = pygame.transform.scale(self.obstacle, (unit, unit))
            case _:
                return
        self.win.blit(img, (start_x + self.border // 2, start_y + self.border // 2))

    def render_general(self, start_x: int, start_y: int, unit: int):
        self.win.blit(
            pygame.transform.scale(self.crown, (unit, unit)),
            (start_x + self.border // 2, start_y + self.border // 2),
        )

    def render_city(self, start_x: int, start_y: int, unit: int):
        pygame.draw.rect(self.win, (128, 128, 128), (start_x, start_y, unit, unit))

        self.win.blit(
            pygame.transform.scale(self.city, (unit, unit)),
            (start_x + self.border // 2, start_y + self.border // 2),
        )

    def render_army(self, start_x: int, start_y: int, unit: int, army: int):
        if army == 0:
            return

        text = self.font.render(str(army), True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(
                start_x + (unit - self.border) // 2,
                start_y + (unit - self.border) // 2,
            )
        )

        self.win.blit(text, text_rect)

    def update(self):
        logger.info("Updating GUI")

        width = self.win.get_width()
        height = self.win.get_height()

        unit = min(width // self._data.width, height // self._data.height)
        block_unit = unit - self.border

        dx = (width - self._data.width * unit) // 2
        dy = (height - self._data.height * unit) // 2

        for i, (army, terrain, is_city, is_general) in enumerate(self._data.map):
            y, x = divmod(i, self._data.width)

            start_x = x * unit + dx
            start_y = y * unit + dy

            self.render_terrain(start_x, start_y, block_unit, terrain)

            if is_general:
                self.render_general(start_x, start_y, block_unit)

            if is_city:
                self.render_city(start_x, start_y, block_unit)

            self.render_army(start_x, start_y, block_unit, army)

        pygame.display.flip()
