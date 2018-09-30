import pygame
import MGUI
import json
from millify import millify_num
from level_map import LevelMap
from map_collection import MapCollection
from .cv_game_playerbuild import PlayerBuildMenu


class CanvasGame(MGUI.GUICanvas):
    def __init__(self, x, y, width, height, player_data):
        super().__init__(x, y, width, height)
        self.player_data = player_data
        self.energy = player_data.start_energy

        # Load base buildings/units
        with open("assets/buildings.json", "r") as file:
            self.base_buildings = json.loads(file.read())
        with open("assets/units.json", "r") as file:
            self.base_units = json.loads(file.read())

        self.backg_widget.set_border(True, (200, 200, 200))

        self.levelmap = LevelMap(0, 0, 12, 8, self.base_buildings, self.base_units)
        self.levelmap.set_visible(False)

        self.map_coll = MapCollection(x, y, width, height, self.levelmap)
        self.add_element(self.map_coll.get_widgets_list())

        self.buildmenu = PlayerBuildMenu(4, 4, 200, height - 8, self.base_buildings, player_data, self.place_building)
        self.buildmenu.set_visible(False)
        self.add_element(self.buildmenu.get_widgets_list())

        font = pygame.font.Font("assets/Dosis.otf", 18)
        # Energy img & label
        self.energy_label = MGUI.Label(width / 2, 8, 0, 0, font, millify_num(self.energy) + " energy")
        self.energy_label.set_text_resize(res_hor=True, res_ver=True, padding=2)
        self.energy_label.set_transparent(True)
        self.energy_label.set_font_color((255, 210, 255))
        self.add_element(self.energy_label, layer=10)

        self.energy_img = MGUI.AnimSprite(0, 0, 0, 0, "assets/materials/energy.png", 4)
        tmp_x = self.energy_label.get_position()[0] - self.energy_img.get_width() - 2
        self.energy_img.set_position(tmp_x, 6)
        self.add_element(self.energy_img)

    def init_data(self, src_tile):
        self.levelmap.load_level(src_tile.region.name, src_tile.level_id)
        self.levelmap.set_visible(True)

    def place_building(self, building_name):
        bdata = self.base_buildings[building_name]
        sel_tile = self.map_coll.selected_tile

        if self.energy >= bdata["cost"]:
            self.energy -= bdata["cost"]
        self.buildmenu.update_data(self.energy)
        self.levelmap.create_building_at(sel_tile.x, sel_tile.y, building_name)

    def handle_event(self, event_list):
        super().handle_event(event_list)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        buildmenu_hovered = self.buildmenu.is_visible() and \
                            self.buildmenu["background"].get_bounds_at(self.x, self.y).collidepoint(mouse_x, mouse_y)

        if not buildmenu_hovered:
            self.map_coll.set_hovered(True)
        else:
            self.map_coll.set_hovered(False)

        self.map_coll.handle_event(event_list)
        self.map_coll.update()

        # Open buildings panel when selecting tile
        sel_tile = self.map_coll.selected_tile
        if sel_tile and sel_tile.owned and not self.levelmap.get_building_at(sel_tile.x, sel_tile.y):
            if not self.buildmenu.is_visible():
                self.buildmenu.set_visible(True)
                self.buildmenu.update_data(self.energy)
        else:
            if self.buildmenu.is_visible():
                self.buildmenu.set_visible(False)

        # Update energy label
        energy_txt = millify_num(self.energy) + " energy"
        if not self.energy_label.get_text() == energy_txt:
            self.energy_label.set_text(energy_txt)