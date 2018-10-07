import pygame, MGUI, json, math
from .cvswitcher import CanvasSwitcher
from millify import millify_num
from level_map import LevelMap
from map_collection import MapCollection
from .cv_game_playerbuild import PlayerBuildMenu
import level_building as buildings
import level_unit as units


class CanvasGame(CanvasSwitcher):
    def __init__(self, x, y, width, height, player_data):
        super().__init__(x, y, width, height)
        self.player_data = player_data
        self.energy = player_data.start_energy
        self.energy_ps = player_data.start_energyps

        self.ticker = 0
        self.paused = False

        # Load base buildings/units
        with open("assets/buildings.json", "r") as file:
            self.base_buildings = json.loads(file.read())
        with open("assets/units.json", "r") as file:
            self.base_units = json.loads(file.read())

        self.backg_widget.set_border(True, (200, 200, 200))

        self.levelmap = LevelMap(0, 0, 0, 0)
        self.levelmap.set_visible(False)

        self.map_coll = MapCollection(x, y, width, height, self.levelmap)
        self.add_element(self.map_coll.get_widgets_list())

        self.buildmenu = PlayerBuildMenu(4, 4, 200, height - 8, self.base_buildings, player_data, self.place_building)
        self.buildmenu.set_visible(False)
        self.add_element(self.buildmenu.get_widgets_list())

        # Buildings data
        self.building_list = []

        # Units data
        self.unit_list = []
        self.unit_layer = MGUI.GUICanvas(0, 0, *self.get_size())
        self.unit_layer.backg_widget.set_transparent(True)

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

        # Paused label
        self.paused_label = MGUI.Label(0, 0, 0, 0, font, "PAUSED")
        self.paused_label.set_text_resize(res_hor=True, res_ver=True, padding=8)
        self.paused_label.set_border(True)
        tmp_x = width / 2 - self.paused_label.get_width() / 2
        tmp_y = height / 2 - self.paused_label.get_height() / 2
        self.paused_label.set_position(tmp_x, tmp_y)
        self.paused_label.set_visible(False)
        self.add_element(self.paused_label, layer=10)

    def init_data(self, source_tile):
        self.paused = True

        self.levelmap.load_level_fromtile(source_tile)
        self.levelmap.set_visible(True)

        self.unit_list = []
        self.building_list = []
        for _ in range(self.levelmap.height):
            self.unit_list.append([])
            self.building_list.append([])
        self.map_coll.center_camera()

        # Load level buildings
        level_buildings = self.levelmap.level_buildings
        for bname in level_buildings:
            building_list = level_buildings[bname]
            for b in building_list:
                self.create_building_at(b[0], b[1], b[2], bname)

    def add_energy(self, mod):
        self.energy += mod
        if self.buildmenu.is_visible():
            self.buildmenu.update_data(self.energy)

    def place_building(self, building_name):
        bdata = self.base_buildings[building_name]
        sel_tile = self.map_coll.selected_tile

        if self.energy >= bdata["cost"]:
            self.add_energy(-bdata["cost"])
        self.create_building_at(sel_tile.x, sel_tile.y, True, building_name)

    def create_building_at(self, x, y, player_owned, building_name):
        building_data = self.base_buildings[building_name]
        new_building = None
        if "type" in building_data:
            # Create building based on type
            b_type = building_data["type"]

            # Unit spawner
            if b_type == buildings.buildtype_spawner:
                new_building = buildings.BuildingSpawner(x, y, player_owned, building_data)

        if not new_building:
            new_building = buildings.Building(x, y, player_owned, building_data)

        self.building_list[y].append(new_building)
        self.add_element(new_building, layer=1)

    def get_building_at(self, x, y):
        for b in self.building_list[y]:
            if b.x == x:
                return b
        return None

    def remove_building(self, building, sell=False):
        if building and building in self.building_list[building.y]:
            if sell:
                if building.player_owned:
                    self.add_energy(math.floor(building.cost * 0.4))
                else:
                    return
            self.building_list[building.y].remove(building)
            self.remove_element(building)

    def create_unit_at(self, x, y, player_owned, unit_name):
        unit_data = self.base_units[unit_name]
        new_unit = units.Unit(x, y, player_owned, unit_data)

        self.unit_list[y].append(new_unit)
        self.add_element(new_unit, layer=2)

    def remove_unit(self, unit):
        if unit in self.unit_list[unit.row]:
            self.unit_list[unit.row].remove(unit)
            self.remove_element(unit)

    def tick(self):
        if self.paused:
            return

        remove_buildings = []
        remove_units = []
        mapx, mapy = self.levelmap.get_position()
        for h in range(self.levelmap.height):
            # Process units
            for u in self.unit_list[h]:
                u.tick()

                u_x, u_y = u.get_position()
                u_w = u.get_width()
                # Process walking units
                if u.state == units.state_walk:
                    # Check for opposing units to battle
                    u_range = 20 + u.get_width() / 2  # TODO change to unit range variable
                    for u_other in self.unit_list[h] + self.building_list[h]:
                        if u is u_other or u_other.player_owned == u.player_owned or u_other.hp <= 0:
                            continue
                        u_otherx, u_othery = u_other.get_position()
                        u_otherw = u_other.get_width()
                        if abs((u_x + u_w / 2) - (u_otherx + u_otherw / 2)) < u_range:
                            u.set_battle_target(u_other)

                    # Check if unit is out of bounds and fade/delete it if so
                    if not u.state == units.state_fade:
                        u_mapx = math.floor(abs(mapx - u_x) / 48)
                        if (u_x and u_x < mapx - 8) or u_mapx >= self.levelmap.width:
                            u.switch_state(units.state_fade)
                # Process battling units
                elif u.state == units.state_battle:
                    if u.is_attack_ready() and u.battle_target:
                        u.battle_target.hurt(u.get_damage())
                        if u.battle_target.hp <= 0:
                            if isinstance(u.battle_target, buildings.Building) and not u.battle_target.player_owned:
                                self.levelmap.enemy_buildings -= 1
                            u.battle_target = None
                            u.switch_state(units.state_walk)
                        else:
                            u.reset_attack()
                # Delete units
                elif u.state == units.state_delete:
                    remove_units.append(u)
            # Process buildings
            for b in self.building_list[h]:
                b.tick()
                if b.type == buildings.buildtype_spawner:
                    if b.is_unit_ready():
                        self.create_unit_at(b.x, b.y, b.player_owned, b.spawn_unit)
                        b.reset_spawn()
                if b.hp <= 0:
                    remove_buildings.append(b)
        for b in remove_buildings:
            self.remove_building(b)
        for u in remove_units:
            self.remove_unit(u)

        self.ticker = (self.ticker + 1) % 60
        if self.ticker == 0:
            self.add_energy(self.energy_ps)

    def handle_event(self, event_list):
        super().handle_event(event_list)

        self.tick()

        sel_tile = self.map_coll.selected_tile

        # Handle events
        for event in event_list:
            if event.type in {pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN}:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                buildmenu_hovered = self.buildmenu.is_visible() and \
                                    self.buildmenu["background"].get_bounds_at(self.x, self.y).collidepoint(mouse_x, mouse_y)

                if not buildmenu_hovered:
                    self.map_coll.set_hovered(True)
                else:
                    self.map_coll.set_hovered(False)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause game
                    self.paused = not self.paused
                elif event.key == pygame.K_DELETE:  # Delete building
                    if sel_tile:
                        self.remove_building(self.get_building_at(sel_tile.x, sel_tile.y), sell=True)

        # Open buildings panel when selecting tile
        if sel_tile and sel_tile.owned and not self.get_building_at(sel_tile.x, sel_tile.y):
            if not self.buildmenu.is_visible():
                self.buildmenu.set_visible(True)
                self.buildmenu.update_data(self.energy)
        else:
            if self.buildmenu.is_visible():
                self.buildmenu.set_visible(False)

        self.map_coll.handle_event(event_list)
        self.map_coll.update()

        cam_x, cam_y = self.map_coll.get_camera_position()
        for h in range(self.levelmap.height):
            # Update buildings
            for b in self.building_list[h]:
                bx, by = b.get_draw_position()
                if not b.get_position() == (bx + cam_x, by + cam_y):
                    b.set_position(bx + cam_x, by + cam_y)

            # Update units
            for u in self.unit_list[h]:
                ux, uy = u.get_draw_position()
                if not u.get_position() == (ux + cam_x, uy + cam_y):
                    u.set_position(ux + cam_x, uy + cam_y)

        # Update energy label
        energy_txt = millify_num(self.energy) + " energy"
        if not self.energy_label.get_text() == energy_txt:
            self.energy_label.set_text(energy_txt)

        # Update pause label
        if not self.paused_label.is_visible() == self.paused:
            self.paused_label.set_visible(self.paused)