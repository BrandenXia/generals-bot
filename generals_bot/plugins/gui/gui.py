import asyncio
import logging
from pathlib import Path

from generals_bot.constant.gui import PLAYER_COLOR_RGB, TERRAIN_COLOR_RGB
from generals_bot.plugins.data import GameData
from generals_bot.types.map import Terrain
from .silent_pygame import silent_pygame

pygame = silent_pygame()

logger = logging.getLogger(__name__)


class GameGUI:
    """
    A GUI for the Generals.io bot, a simple pygame GUI that displays the game map and some basic information,
    not interactive and is only used for debugging purposes
    """

    def __init__(self) -> None:
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

        logger.info("GameGUI initialized")

    def _init_screen(self) -> None:
        """Fill the screen with a dark grey color and display the title of the game"""
        self.win.fill((34, 34, 34))
        self.win.blit(
            self.font.render("Generals.io Bot", True, (255, 255, 255)), (10, 10)
        )
        pygame.display.flip()

    def game_over(self) -> None:
        """Display a game over message"""
        self.win.blit(self.font.render("Game Over", True, (255, 255, 255)), (10, 70))
        pygame.display.flip()

    def reset(self) -> None:
        """Reset the screen, used when a new game starts"""
        self._init_screen()
        self._data = None

    def set_data(self, data: GameData) -> None:
        """Set reference to the game data, be called at the start of each game"""
        self._data = data

    @staticmethod
    async def pygame_event_loop() -> None:
        """Start the pygame event loop, this is a coroutine that runs indefinitely until the window is closed"""
        logger.info("Starting pygame event loop")
        while True:
            await asyncio.sleep(0)
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break
        pygame.quit()
        logger.info("Stopped pygame event loop")

    def update(self) -> None:
        """Update the GUI with the current game state"""
        self._render_turn()
        self._render_map()

    def _render_turn(self) -> None:
        """Display the current turn number"""
        self.win.fill((34, 34, 34), (0, 30, 200, 40))
        text = self.font.render(f"Turn: {self._data.turn}", True, (255, 255, 255))
        self.win.blit(text, (10, 40))

    def _render_map(self) -> None:
        """Render the game map"""
        logger.info("Updating GUI")

        width = self.win.get_width()
        height = self.win.get_height()

        unit = min(width // self._data.map.width, height // self._data.map.height)
        block_unit = unit - self.border

        dx = (width - self._data.map.width * unit) // 2
        dy = (height - self._data.map.height * unit) // 2

        for x, y, army, terrain, is_city, is_general in self._data.map[
            :, :, ("x", "y", "army", "terrain", "is_city", "is_general")
        ]:
            start_x = x * unit + dx
            start_y = y * unit + dy

            self._render_terrain(start_x, start_y, block_unit, terrain)

            if is_general:
                self._render_general(start_x, start_y, block_unit)

            if is_city:
                self._render_city(start_x, start_y, block_unit)

            self._render_army(start_x, start_y, block_unit, army)

        pygame.display.flip()

    def _render_terrain(
        self, start_x: int, start_y: int, unit: int, terrain: Terrain
    ) -> None:
        """Render a block of terrain on the screen"""
        color = (
            PLAYER_COLOR_RGB[terrain]
            if terrain.is_player
            else TERRAIN_COLOR_RGB[terrain]
        )

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

    def _render_general(self, start_x: int, start_y: int, unit: int) -> None:
        """Render a crown on the screen to indicate the general's location"""
        self.win.blit(
            pygame.transform.scale(self.crown, (unit, unit)),
            (start_x + self.border // 2, start_y + self.border // 2),
        )

    def _render_city(self, start_x: int, start_y: int, unit: int) -> None:
        """Render a city on the screen to indicate the city's location"""
        pygame.draw.rect(self.win, (128, 128, 128), (start_x, start_y, unit, unit))

        self.win.blit(
            pygame.transform.scale(self.city, (unit, unit)),
            (start_x + self.border // 2, start_y + self.border // 2),
        )

    def _render_army(self, start_x: int, start_y: int, unit: int, army: int) -> None:
        """Render the army count on the screen"""
        if army == 0:
            return

        text = self.font.render(str(army), True, (255, 255, 255))
        text_rect = text.get_rect(center=(start_x + unit // 2, start_y + unit // 2))

        self.win.blit(text, text_rect)
