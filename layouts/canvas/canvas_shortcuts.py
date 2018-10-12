import pygame
import MGUI
from .cvswitcher import CanvasSwitcher


class CanvasShortcuts(CanvasSwitcher):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (0, 0, 50))

        # Variables
        self.sel_shortcut = "terrain"

        self.backg_widget.set_border(True, (0, 0, 150))

        font = pygame.font.Font("assets/Dosis.otf", 18)

        tmp_x = 12
        # Terrain button
        self.button_terrain = MGUI.Button(tmp_x, 10, 0, 26, font, "Terrain")
        self.button_terrain.set_callback(self.switch_target, ["terrain"])
        self.button_terrain.set_text_resize(res_hor=True, padding=8)
        self.button_terrain.set_font_color((0, 200, 0))
        self.button_terrain.set_border(True, (50, 100, 50))
        self.button_terrain.set_hovered_color((100, 100, 100, 80))
        self.button_terrain.set_pressed_color((100, 100, 100, 150))
        self.add_element(self.button_terrain)

        tmp_x += self.button_terrain.get_width() + 12
        # Upgrades button
        self.button_buildings = MGUI.Button(tmp_x, 10, 0, 26, font, "Buildings")
        self.button_buildings.set_callback(self.switch_target, ["buildings"])
        self.button_buildings.set_text_resize(res_hor=True, padding=8)
        self.button_buildings.set_font_color((0, 200, 200))
        self.button_buildings.set_border(True, (50, 100, 100))
        self.button_buildings.set_hovered_color((100, 100, 100, 80))
        self.button_buildings.set_pressed_color((100, 100, 100, 150))
        self.add_element(self.button_buildings)

        tmp_x += self.button_buildings.get_width() + 12
        # Save game button
        self.button_save = MGUI.Button(tmp_x, 10, 0, 26, font, "Save")
        self.button_save.set_callback(self.switch_target, ["savegame"])
        self.button_save.set_text_resize(res_hor=True, padding=8)
        self.button_save.set_font_color((255, 102, 0))
        self.button_save.set_border(True, (255, 100, 50))
        self.button_save.set_hovered_color((100, 100, 100, 80))
        self.button_save.set_pressed_color((100, 100, 100, 150))
        self.add_element(self.button_save)

        tmp_x += self.button_save.get_width() + 12
        # Load game button
        self.button_load = MGUI.Button(tmp_x, 10, 0, 26, font, "Load")
        self.button_load.set_callback(self.switch_target, ["loadgame"])
        self.button_load.set_text_resize(res_hor=True, padding=8)
        self.button_load.set_font_color((255, 102, 0))
        self.button_load.set_border(True, (255, 100, 50))
        self.button_load.set_hovered_color((100, 100, 100, 80))
        self.button_load.set_pressed_color((100, 100, 100, 150))
        self.add_element(self.button_load)