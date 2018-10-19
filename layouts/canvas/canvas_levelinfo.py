import pygame
import MGUI
import json
from level_map import LevelMap
from .cvswitcher import CanvasSwitcher
from millify import millify_num
import level_building as buildings


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

        tmp_y = self.title_label.get_height() + 8
        # Preview label
        self.preview_label = MGUI.Label(16, tmp_y, 0, 0, font_21, "Level preview:")
        self.preview_label.set_text_resize(res_hor=True, res_ver=True)
        self.preview_label.set_transparent(True)
        self.preview_label.set_font_color((255, 100, 255))
        self.add_element(self.preview_label)

        tmp_y += self.preview_label.get_height() + 4
        # Level preview box
        self.previewbox = MGUI.ImageWidget(16, tmp_y, 128, 128)
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

        new_button = BuildingButton(new_x, self.building_buttons_y, bdata, bname, amount, self.base_units)
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
            for w in b.get_widgets_list():
                self.remove_element(w[0])
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
    def __init__(self, x, y, bdata, bname, amount, bunits):
        super().__init__()

        font_12 = pygame.font.Font("assets/Dosis.otf", 14)
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
        tmp_y += 8
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

        tmp_x, tmp_y = build_image.get_position()
        tmp_y += build_image.get_height() + 1
        # Spawner unit info
        if bdata["type"] == buildings.buildtype_spawner:
            unitsp = bunits[bdata["spawn_unit"]]
            unitsp_imgdata = unitsp["img_data"]

            # Unit name label
            unitsp_label = MGUI.Label(tmp_x, tmp_y, buildinfo_frame.get_width() - 4, 0, font_21, bdata["spawn_unit"])
            unitsp_label.set_text_resize(res_ver=True)
            unitsp_label.set_transparent(True)
            unitsp_label.set_border(True, (255, 100, 255))
            self.add_widget(unitsp_label, "unitsp_label")

            # Animated unit image
            tmp_y += unitsp_label.get_height() + 1
            unitsp_image = MGUI.AnimSprite(tmp_x, tmp_y, *build_image.get_size(),
                                           icon="assets/units/" + unitsp_imgdata["img"],
                                           frames=unitsp_imgdata["frames"],
                                           autosize=False)
            if "animations" in unitsp_imgdata and "base" in unitsp_imgdata["animations"]:
                unitsp_image.set_animation_data({"base": unitsp_imgdata["animations"]["base"]})
            unitsp_image.set_border(True, (255, 100, 255))
            self.add_widget(unitsp_image, "unitsp_image")

            tmp_y += 2
            tmp_x += unitsp_image.get_width() + 4
            # Unit health icon
            unithealth_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/heart.png", smooth=True)
            unithealth_img.set_icon_autoscale(True)
            self.add_widget(unithealth_img, "unithealth_img")

            tmp_x += unithealth_img.get_width() + 4
            # Unit health label
            unithealth_label = MGUI.Label(tmp_x, tmp_y - 1, 0, 0, font_16, millify_num(unitsp["maxhp"]))
            unithealth_label.set_text_resize(res_hor=True, res_ver=True)
            unithealth_label.set_transparent(True)
            unithealth_label.set_font_color((255, 110, 110))
            self.add_widget(unithealth_label, "unithealth_label")

            tmp_x += unithealth_label.get_width() + 8
            # Unit speed icon
            unitspeed_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/speed_boot.png")
            unitspeed_img.set_icon_autoscale(True)
            self.add_widget(unitspeed_img, "unitspeed_img")

            tmp_x += unitspeed_img.get_width() + 4
            # Unit speed label
            unitspeed_label = MGUI.Label(tmp_x, tmp_y - 1, 0, 0, font_16, millify_num(unitsp["speed"]))
            unitspeed_label.set_text_resize(res_hor=True, res_ver=True)
            unitspeed_label.set_transparent(True)
            unitspeed_label.set_font_color((110, 255, 110))
            self.add_widget(unitspeed_label, "unitspeed_label")

            tmp_x = unithealth_img.get_position()[0]
            tmp_y += unithealth_img.get_height() + 2
            # Unit damage to player icon
            unit_pldmg_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/escape.png")
            unit_pldmg_img.set_icon_autoscale(True)
            self.add_widget(unit_pldmg_img, "unit_pldmg_img")

            tmp_x += unit_pldmg_img.get_width() + 4
            # Unit damage to player label
            unit_pldmg_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, millify_num(unitsp["dmg_player"]))
            unit_pldmg_label.set_text_resize(res_ver=True, res_hor=True)
            unit_pldmg_label.set_transparent(True)
            unit_pldmg_label.set_font_color((255, 255, 110))
            self.add_widget(unit_pldmg_label, "unit_pldmg_label")

            # region ---- UNIT DAMAGE TYPES INFORMATION ----
            tmp_x, tmp_y = unitsp_image.get_position()
            tmp_x += 2
            tmp_y += unitsp_image.get_height() + 4
            # Unit physical damage icon
            unit_physdmg_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/attack_swords.png")
            unit_physdmg_img.set_icon_autoscale(True)
            self.add_widget(unit_physdmg_img, "unit_physdmg_img")

            tmp_x += unit_physdmg_img.get_width() + 4
            # Unit physical damage label
            tmp_text = "0"
            if "dmg_phys" in unitsp:
                tmp_text = millify_num(unitsp["dmg_phys"])
            unit_physdmg_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, tmp_text)
            unit_physdmg_label.set_text_resize(res_hor=True, res_ver=True)
            unit_physdmg_label.set_transparent(True)
            self.add_widget(unit_physdmg_label, "unit_physdmg_label")

            tmp_x += unit_physdmg_label.get_width() + 8
            # Unit fire damage image
            unit_firedmg_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/firedmg_swords.png")
            unit_firedmg_img.set_icon_autoscale(True)
            self.add_widget(unit_firedmg_img, "unit_firedmg_img")

            tmp_x += unit_firedmg_img.get_width() + 4
            tmp_text = "0"
            if "dmg_fire" in unitsp:
                tmp_text = millify_num(unitsp["dmg_fire"])
            # Unit fire damage label
            unit_firedmg_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, tmp_text)
            unit_firedmg_label.set_text_resize(res_hor=True, res_ver=True)
            unit_firedmg_label.set_transparent(True)
            unit_firedmg_label.set_font_color((255, 180, 110))
            self.add_widget(unit_firedmg_label, "unit_firedmg_label")

            tmp_x += unit_firedmg_label.get_width() + 8
            # Unit cold damage image
            unit_colddmg_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/colddmg_swords.png")
            unit_colddmg_img.set_icon_autoscale(True)
            self.add_widget(unit_colddmg_img, "unit_colddmg_img")

            tmp_x += unit_colddmg_img.get_width() + 4
            tmp_text = "0"
            if "dmg_cold" in unitsp:
                tmp_text = millify_num(unitsp["dmg_cold"])
            # Unit cold damage label
            unit_colddmg_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, tmp_text)
            unit_colddmg_label.set_text_resize(res_hor=True, res_ver=True)
            unit_colddmg_label.set_transparent(True)
            unit_colddmg_label.set_font_color((110, 200, 255))
            self.add_widget(unit_colddmg_label, "unit_colddmg_label")

            tmp_x += unit_colddmg_label.get_width() + 8
            # Unit lightning damage image
            unit_lningdmg_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/lightningdmg_swords.png")
            unit_lningdmg_img.set_icon_autoscale(True)
            self.add_widget(unit_lningdmg_img, "unit_lningdmg_img")

            tmp_x += unit_lningdmg_img.get_width() + 4
            tmp_text = "0"
            if "dmg_lightning" in unitsp:
                tmp_text = millify_num(unitsp["dmg_lightning"])
            # Unit lightning damage label
            unit_lningdmg_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, tmp_text)
            unit_lningdmg_label.set_text_resize(res_hor=True, res_ver=True)
            unit_lningdmg_label.set_transparent(True)
            unit_lningdmg_label.set_font_color((255, 200, 110))
            self.add_widget(unit_lningdmg_label, "unit_lningdmg_label")
            # endregion

            # region ---- UNIT RESISTANCE TYPES INFORMATION ----
            tmp_x = unit_physdmg_img.get_position()[0]
            tmp_y += unit_physdmg_img.get_height() + 1
            # Unit armor image
            unitarmor_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/armor.png")
            unitarmor_img.set_icon_autoscale(True)
            self.add_widget(unitarmor_img, "unitarmor_img")

            tmp_x += unitarmor_img.get_width() + 4
            tmp_text = "0"
            if "armor" in unitsp:
                tmp_text = millify_num(unitsp["armor"])
            # Unit armor label
            unitarmor_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, tmp_text)
            unitarmor_label.set_text_resize(res_hor=True, res_ver=True)
            unitarmor_label.set_transparent(True)
            self.add_widget(unitarmor_label, "unitarmor_label")

            tmp_x += unitarmor_label.get_width() + 8
            # Unit fire resistance image
            unit_fireres_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/fire_res.png")
            unit_fireres_img.set_icon_autoscale(True)
            self.add_widget(unit_fireres_img, "unit_fireres_img")

            tmp_x += unit_fireres_img.get_width() + 4
            tmp_text = "0"
            if "res_fire" in unitsp:
                tmp_text = millify_num(unitsp["res_fire"])
            # Unit fire resistance label
            unit_fireres_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, tmp_text)
            unit_fireres_label.set_text_resize(res_hor=True, res_ver=True)
            unit_fireres_label.set_transparent(True)
            unit_fireres_label.set_font_color(unit_firedmg_label.get_font_color())
            self.add_widget(unit_fireres_label, "unit_fireres_label")

            tmp_x += unit_fireres_label.get_width() + 8
            # Unit cold resistance image
            unit_coldres_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/cold_res.png")
            unit_coldres_img.set_icon_autoscale(True)
            self.add_widget(unit_coldres_img, "unit_coldres_img")

            tmp_x += unit_coldres_img.get_width() + 4
            tmp_text = "0"
            if "res_cold" in unitsp:
                tmp_text = millify_num(unitsp["res_cold"])
            # Unit cold resistance label
            unit_coldres_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, tmp_text)
            unit_coldres_label.set_text_resize(res_hor=True, res_ver=True)
            unit_coldres_label.set_transparent(True)
            unit_coldres_label.set_font_color(unit_colddmg_label.get_font_color())
            self.add_widget(unit_coldres_label, "unit_coldres_label")

            tmp_x += unit_coldres_label.get_width() + 8
            # Unit lightning resistance image
            unit_lningres_img = MGUI.ImageWidget(tmp_x, tmp_y, 18, 18, "assets/UI/lightning_res.png")
            unit_lningres_img.set_icon_autoscale(True)
            self.add_widget(unit_lningres_img, "unit_lningres_img")

            tmp_x += unit_lningres_img.get_width() + 4
            tmp_text = "0"
            if "res_lightning" in unitsp:
                tmp_text = millify_num(unitsp["res_lightning"])
            # Unit lightning resistance label
            unit_lningres_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_16, tmp_text)
            unit_lningres_label.set_text_resize(res_hor=True, res_ver=True)
            unit_lningres_label.set_transparent(True)
            unit_lningres_label.set_font_color(unit_lningdmg_label.get_font_color())
            self.add_widget(unit_lningres_label, "unit_lningres_label")
            # endregion