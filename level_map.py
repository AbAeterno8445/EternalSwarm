import pygame
from game_map import GameMap, MapTile
import level_building as buildings


class LevelMap(GameMap):
    def __init__(self, x, y, width, height, base_buildings, base_units):
        super().__init__(x, y, width, height)

        self.level_surface = pygame.Surface((self.get_width() + 32, self.get_height() + 32)).convert()
        self.level_surface.set_colorkey((0, 0, 0))

        self.base_buildings = base_buildings
        self.base_units = base_units

        # Buildings data
        self.building_list = []
        self.update_building_layer = False
        self.building_layer = pygame.Surface(self.get_size()).convert()
        self.building_layer.set_colorkey((0, 0, 0))

    def load_level(self, region_name, level_id):
        region_name = region_name.lower()
        self.load_regions_json("levels/" + region_name + "/regions.json", False)
        lvl_path = "levels/" + region_name + "/level" + str(level_id)
        with open(lvl_path, "r") as file:
            # Load level size
            tmp_size = file.readline().strip().split(',')
            self.width = int(tmp_size[0])
            self.height = int(tmp_size[1])

            tmp_regionmap = []
            for i in range(self.height):
                tmp_regionmap.append(file.readline().strip().split(','))

            self.map_data.clear()
            for i in range(self.height):
                self.map_data.append([])
                for j in range(self.width):
                    region_id = int(tmp_regionmap[i][j])
                    tmp_tile = MapTile(j, i, self.regions[region_id])
                    if j < 3:
                        tmp_tile.owned = True
                    self.map_data[i].append(tmp_tile)

        self.update_tilemap()

    def update_tilemap(self):
        super().update_tilemap()
        self.update_layers(tiles=True, buildings=False, units=False)

    def update_layers(self, tiles, buildings, units):
        if tiles:
            self.level_surface.blit(self.tilemap_surface, (0, 0))
        if buildings:
            self.level_surface.blit(self.building_layer, (0, 0))
        self.mark_dirty()

    def create_building_at(self, x, y, player_owned, building_name):
        new_building = self.base_buildings[building_name]
        tmp_building = None
        if "type" in new_building:
            # Create building based on type
            b_type = new_building["type"]

            # Unit spawner
            if b_type == buildings.buildtype_spawner:
                tmp_building = buildings.BuildingSpawner(x, y, player_owned, new_building)

        if not tmp_building:
            tmp_building = buildings.Building(x, y, player_owned, new_building)

        self.building_list.append(tmp_building)
        self.update_buildings_layer()

    def update_buildings_layer(self):
        self.building_layer.fill((0, 0, 0))
        for b in self.building_list:
            self.building_layer.blit(b._get_appearance(), b.get_draw_position())
        self.update_layers(tiles=True, buildings=True, units=True)

    def tick(self):
        for b in self.building_list:
            b.tick()

    def get_building_at(self, x, y):
        for b in self.building_list:
            if b.x == x and b.y == y:
                return b
        return None

    def _get_appearance(self, *args):
        return self.level_surface