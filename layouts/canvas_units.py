import pygame
import MSGUI


class CanvasUnits(MSGUI.GUICanvas):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (50, 0, 0))

        self.backg_widget.set_border(True, (150, 0, 0))

        font = pygame.font.Font("assets/Dosis.otf", 18)
        self.test = MSGUI.Label(16, 16, 200, 22, font, "Units - WIP test")
        self.test.set_transparent(True)
        self.add_element(self.test)