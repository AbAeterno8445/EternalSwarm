import pygame
import MGUI
import json
from level_map import LevelMap
from .cvswitcher import CanvasSwitcher
from millify import millify_num


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
        self.title_label.set_font_color((255, 100, 255))
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
        # Enemy buildings label
        self.buildings_label = MGUI.Label(16, tmp_y, 0, 0, font_21, "Enemy buildings:")
        self.buildings_label.set_text_resize(res_hor=True, res_ver=True)
        self.buildings_label.set_transparent(True)
        self.buildings_label.set_font_color((255, 100, 255))
        self.add_element(self.buildings_label)

        tmp_y += self.buildings_label.get_height() + 8
        # List for enemy building buttons
        self.building_buttons = []
        self.building_buttons_y = tmp_y

        # Capture button
        self.capture_button = MGUI.Button(width / 2 + 2, height - 46, 200, 30, font_21, "Capture")
        self.capture_button.set_callback(self.switch_target, ["game"])
        self.capture_button.set_border(True, (255, 100, 255))
        self.capture_button.set_hovered_color((150, 50, 150, 100))
        self.capture_button.set_pressed_color((100, 20, 100, 150))
        self.add_element(self.capture_button)

        tmp_x, tmp_y = self.capture_button.get_position()
        tmp_x -= self.capture_button.get_width() + 4
        # Return button
        self.return_button = MGUI.Button(tmp_x, tmp_y, 200, 30, font_21, "Return")
        self.return_button.set_callback(self.switch_target, ["main"])
        self.return_button.set_border(True, (255, 100, 255))
        self.return_button.set_hovered_color((150, 50, 150, 100))
        self.return_button.set_pressed_color((100, 20, 100, 150))
        self.add_element(self.return_button)

    # Create button for a building
    def _create_building_button(self, bname, amount):
        bdata = self.base_buildings[bname]
        # Calculate position for new button
        new_x = 16
        for b in self.building_buttons:
            new_x += 16 + b.total_width

        new_button = BuildingButton(new_x, self.building_buttons_y, bdata, bname, amount)
        self.building_buttons.append(new_button)
        self.add_element(new_button.get_widgets_list())

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

        for b in self.building_buttons:
            self.remove_element(b.get_widgets_list())
        self.building_buttons.clear()
        # Draw buildings
        for bname in self.levelmap.level_buildings:
            bdata = self.base_buildings[bname]
            building_list = self.levelmap.level_buildings[bname]
            for b in building_list:
                pygame.draw.rect(previewbox_surface, bdata["map_color"], (b[0] * 8, b[1] * 8, 8, 8))

            # Add building button
            self._create_building_button(bname, len(building_list))

        self.previewbox.set_icon(previewbox_surface)

        # Update labels with level information
        self.region_label.set_text("Region: %s" % source_tile.region.name)
        self.levelsize_label.set_text("Size: %i x %i" % (self.levelmap.width, self.levelmap.height))
        self.leveldiff_label.set_text("Hazard level: %i" % source_tile.difficulty)


class BuildingButton(MGUI.WidgetCollection):
    def __init__(self, x, y, bdata, bname, amount):
        super().__init__()

        font_16 = pygame.font.Font("assets/Dosis.otf", 16)
        font_21 = pygame.font.Font("assets/Dosis.otf", 21)

        self.total_width = 191

        # Building info frame
        buildinfo_frame = MGUI.Widget(x, y, self.total_width, 234)
        buildinfo_frame.set_transparent(True)
        buildinfo_frame.set_border(True, (255, 100, 255))
        self.add_widget(buildinfo_frame, "buildinfo_frame")

        tmp_x = x + 2
        tmp_y = y + 2
        # Building map icon reference
        build_mapicon = MGUI.Widget(tmp_x, tmp_y, 28, 28)
        build_mapicon.set_background(bdata["map_color"])
        self.add_widget(build_mapicon, "build_mapicon")

        tmp_width = buildinfo_frame.get_width() - 5 - build_mapicon.get_width()
        # Building name
        build_name_label = MGUI.Label(tmp_x + build_mapicon.get_width() + 1, tmp_y, tmp_width,
                                      build_mapicon.get_height(), font_21, bname)
        build_name_label.set_transparent(True)
        build_name_label.set_border(True, (255, 100, 255))
        self.add_widget(build_name_label, "build_name_label", layer=1)

        tmp_y += build_name_label.get_height() + 1
        # Building image
        build_image = MGUI.ImageWidget(tmp_x, tmp_y, 64, 64, "assets/buildings/" + bdata["base_img"])
        build_image.set_border(True, (255, 100, 255))
        self.add_widget(build_image, "build_image")

        tmp_x += build_image.get_width() + 4
        # Building health
        build_health_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, "Health: " + millify_num(bdata["maxhp"]))
        build_health_label.set_transparent(True)
        build_health_label.set_text_resize(res_hor=True, res_ver=True)
        self.add_widget(build_health_label, "build_health_label")

        tmp_y += build_health_label.get_height() + 2
        # Building amount in level
        build_amt_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, "Amount in level: " + str(amount))
        build_amt_label.set_transparent(True)
        build_amt_label.set_text_resize(res_hor=True, res_ver=True)
        self.add_widget(build_amt_label, "build_amt_label")