import pygame
import MSGUI


class Building(object):
    def __init__(self, x, y, building_data=None):
        self.x = x
        self.y = y
        self.surface = pygame.Surface((48, 48)).convert()
        self.surface.set_colorkey((0, 0, 0))
        self.base_img = MSGUI.ImageWidget(8 + x * 48, 8 + y * 48, 48, 48)

        if building_data:
            self.load_building(building_data)

    def load_building(self, building_data):
        for attr in building_data:
            if attr == "base_img":
                self.base_img.set_icon("assets/buildings/bases/" + building_data[attr])
            elif hasattr(self, attr):
                setattr(self, attr, building_data[attr])

    def get_image(self):
        self.surface.blit(self.base_img._get_appearance(), (0, 0))
        return self.surface

    def get_draw_position(self):
        return self.base_img.get_position()