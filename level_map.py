import pygame
import json
from game_map import GameMap, MapTile
import level_building as buildings


class LevelMap(GameMap):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        # Load base buildings/units
        with open("assets/buildings.json", "r") as file:
            self.base_buildings = json.loads(file.read())
        with open("assets/units.json", "r") as file:
            self.base_units = json.loads(file.read())

        # Buildings data
        self.building_list = []
        # Surface
        self.building_layer = pygame.Surface(self.get_size()).convert()
        self.building_layer.set_colorkey((0, 0, 0))

        for i in range(8):
            for j in range(12):
                self.create_building_at(j, i, "Slime Spawner")

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
                    tmp_tile = LevelTile(j, i, self.regions[region_id])
                    if j < 3:
                        tmp_tile.owned = True
                    self.map_data[i].append(tmp_tile)

        self.update_tilemap()

    def create_building_at(self, x, y, building_name):
        new_building = self.base_buildings[building_name]
        tmp_building = None
        if "type" in new_building:
            # Create building based on type
            b_type = new_building["type"]

            # Unit spawner
            if b_type == buildings.buildtype_spawner:
                tmp_building = buildings.BuildingSpawner(x, y, new_building)
                # Set unit
                tmp_building.set_spawn_unit(self.base_units[tmp_building.spawn_unit])

        if not tmp_building:
            tmp_building = buildings.Building(x, y, new_building)

        self.building_list.append(tmp_building)
        self.update_building_layer()

    def update_building_layer(self):
        self.building_layer.fill((0, 0, 0))
        for b in self.building_list:
            self.building_layer.blit(b._get_appearance(), b.get_draw_position())
        self.mark_dirty()

    def _get_appearance(self, *args):
        surface = super()._get_appearance(*args)
        surface.blit(self.building_layer, (0, 0))
        return surface


class LevelTile(MapTile):
    def __init__(self, x, y, region):
        super().__init__(x, y, region, 0)