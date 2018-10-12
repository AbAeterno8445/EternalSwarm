import pygame
import MGUI
from .cvswitcher import CanvasSwitcher


class CanvasLoadGame(CanvasSwitcher):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (70, 25, 0))

        self.backg_widget.set_border(True, (204, 102, 0))

        font_16 = pygame.font.Font("assets/Dosis.otf", 16)
        font_21 = pygame.font.Font("assets/Dosis.otf", 21)
        font_36 = pygame.font.Font("assets/Dosis.otf", 36)

        # Title
        self.title_label = MGUI.Label(0, 0, 0, 0, font_36, "Load Game")
        self.title_label.set_text_resize(res_hor=True, res_ver=True, padding=8)
        self.title_label.set_position(width / 2 - self.title_label.get_width() / 2, 4)
        self.title_label.set_transparent(True)
        self.title_label.set_font_color((255, 122, 0))
        self.add_element(self.title_label)