import pygame
import json
from game_map import GameMap, MapTile
from level_building import Building


class LevelMap(GameMap):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.level_surface = pygame.Surface(self._bounds.size).convert()
        self.level_surface.set_colorkey((0, 0, 0))

        self.building_list = []
        with open("assets/buildings.json", "r") as file:
            tmp_buildings = json.loads(file.read())
        for b in tmp_buildings:
            self.create_building_at(2, 3, b)

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
                    self.map_data[i].append(tmp_tile)

        self.update_tilemap()

    def create_building_at(self, x, y, building_dict):
        tmp_building = Building(x, y, building_dict)
        self.building_list.append(tmp_building)

    def _get_appearance(self, *args):
        surface = super()._get_appearance(*args)
        self.level_surface.blit(surface, (0, 0))
        for b in self.building_list:
            self.level_surface.blit(b.get_image(), b.get_draw_position())
        return self.level_surface


class LevelTile(MapTile):
    def __init__(self, x, y, region):
        super().__init__(x, y, region, 0)