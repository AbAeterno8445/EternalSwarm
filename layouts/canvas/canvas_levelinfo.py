import pygame
import MGUI
from level_map import LevelMap
from .cvswitcher import CanvasSwitcher


class CanvasLevelInfo(CanvasSwitcher):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (40, 0, 40))

        self.backg_widget.set_border(True, (110, 40, 110))

        self.level_tile = None
        self.levelmap = LevelMap(0, 0, 0, 0)

        font = pygame.font.Font("assets/Dosis.otf", 18)
        self.capture_button = MGUI.Button(32, 32, 200, 200, font, "Capture")
        self.capture_button.set_border(True)
        self.capture_button.set_hovered_color((150, 150, 150, 100))
        self.capture_button.set_pressed_color((100, 100, 100, 150))
        self.add_element(self.capture_button)