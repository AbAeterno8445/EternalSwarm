import pygame
import MGUI


class CanvasShortcuts(MGUI.GUICanvas):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (0, 0, 50))

        # Variables
        self.sel_shortcut = "terrain"

        self.backg_widget.set_border(True, (0, 0, 150))

        font = pygame.font.Font("assets/Dosis.otf", 18)
        # Terrain button
        self.button_terrain = MGUI.Button(12, 10, 0, 26, font, "Terrain")
        self.button_terrain.set_callback(self._switch_canvas, ["terrain"])
        self.button_terrain.set_text_resize(res_hor=True, padding=8)
        self.button_terrain.set_font_color((0, 200, 0))
        self.button_terrain.set_border(True, (50, 100, 50))
        self.button_terrain.set_hovered_color((100, 100, 100, 80))
        self.button_terrain.set_pressed_color((100, 100, 100, 150))
        self.add_element(self.button_terrain)

        tmp_x = self.button_terrain.get_width() + 24
        # Upgrades button
        self.button_upgrades = MGUI.Button(tmp_x, 10, 0, 26, font, "Units")
        self.button_upgrades.set_callback(self._switch_canvas, ["units"])
        self.button_upgrades.set_text_resize(res_hor=True, padding=8)
        self.button_upgrades.set_font_color((0, 200, 200))
        self.button_upgrades.set_border(True, (50, 100, 100))
        self.button_upgrades.set_hovered_color((100, 100, 100, 80))
        self.button_upgrades.set_pressed_color((100, 100, 100, 150))
        self.add_element(self.button_upgrades)

    def get_sel_shortcut(self):
        return self.sel_shortcut

    def _switch_canvas(self, canvas_name):
        self.sel_shortcut = canvas_name