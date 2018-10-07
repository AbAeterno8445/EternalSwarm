import pygame
import MGUI
import json
from level_map import LevelMap
from .cvswitcher import CanvasSwitcher


class CanvasLevelInfo(CanvasSwitcher):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (40, 0, 40))

        self.backg_widget.set_border(True, (110, 40, 110))

        self.level_tile = None
        self.levelmap = LevelMap(0, 0, 0, 0)

        # Load base buildings/units
        with open("assets/buildings.json", "r") as file:
            self.base_buildings = json.loads(file.read())
        with open("assets/units.json", "r") as file:
            self.base_units = json.loads(file.read())

        font_21 = pygame.font.Font("assets/Dosis.otf", 21)
        font_36 = pygame.font.Font("assets/Dosis.otf", 36)

        # Title
        self.title_label = MGUI.Label(0, 0, 0, 0, font_36, "Terrain Information")
        self.title_label.set_text_resize(res_hor=True, res_ver=True, padding=4)
        tmp_x = width / 2 - self.title_label.get_width() / 2
        self.title_label.set_position(tmp_x, 4)
        self.title_label.set_transparent(True)
        self.add_element(self.title_label)

        # Level preview box
        self.previewbox = MGUI.ImageWidget(16, 96, 128, 128)
        self.previewbox.set_transparent(False)
        self.previewbox.set_icon_autoscale(True)
        self.previewbox.set_border(True)
        self.add_element(self.previewbox)

        tmp_x, tmp_y = self.previewbox.get_position()
        tmp_x += self.previewbox.get_width() + 16
        # Level region label
        self.region_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_21, "Region:")
        self.region_label.set_text_resize(res_hor=True, res_ver=True, padding=4)
        self.region_label.set_transparent(True)
        self.add_element(self.region_label)

        tmp_y += self.region_label.get_height() + 4
        # Level size label
        self.levelsize_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_21, "Size:")
        self.levelsize_label.set_text_resize(res_hor=True, res_ver=True, padding=4)
        self.levelsize_label.set_transparent(True)
        self.add_element(self.levelsize_label)

        tmp_y += self.levelsize_label.get_height() + 4
        # Level difficulty label
        self.leveldiff_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_21, "Hazard level:")
        self.leveldiff_label.set_text_resize(res_hor=True, res_ver=True, padding=4)
        self.leveldiff_label.set_transparent(True)
        self.add_element(self.leveldiff_label)

        tmp_y = self.previewbox.get_position()[1] + self.previewbox.get_height() + 16
        # Buildings in level table
        self.building_label = MGUI.Label(16, tmp_y, 0, 0, font_21, "Building")

        # Capture button
        self.capture_button = MGUI.Button(width / 2 - 100, height - 46, 200, 30, font_21, "Capture")
        self.capture_button.set_callback(self.switch_target, ["game"])
        self.capture_button.set_border(True)
        self.capture_button.set_hovered_color((150, 150, 150, 100))
        self.capture_button.set_pressed_color((100, 100, 100, 150))
        self.add_element(self.capture_button)

    def init_data(self, source_tile):
        self.level_tile = source_tile
        self.levelmap.load_level_fromtile(source_tile, update_levelmap=False)

        # Initialize previewbox
        previewbox_surface = pygame.Surface((8 * self.levelmap.width, 8 * self.levelmap.height)).convert()
        previewbox_surface.fill((0, 0, 0))

        # Draw map tiles
        for i in range(self.levelmap.height):
            for j in range(self.levelmap.width):
                cur_tile = self.levelmap.get_tile_at(j, i)
                tile_color = cur_tile.region.color
                if cur_tile.owned:
                    tile_color = (255, 255, 0)
                pygame.draw.rect(previewbox_surface, tile_color, (j * 8, i * 8, 8, 8))
        # Draw buildings
        for bname in self.levelmap.level_buildings:
            bdata = self.base_buildings[bname]
            building_list = self.levelmap.level_buildings[bname]
            for b in building_list:
                pygame.draw.rect(previewbox_surface, bdata["map_color"], (b[0] * 8, b[1] * 8, 8, 8))

        self.previewbox.set_icon(previewbox_surface)

        # Update labels with level information
        self.region_label.set_text("Region: %s" % source_tile.region.name)
        self.levelsize_label.set_text("Size: %i x %i" % (self.levelmap.width, self.levelmap.height))
        self.leveldiff_label.set_text("Hazard level: %i" % source_tile.difficulty)