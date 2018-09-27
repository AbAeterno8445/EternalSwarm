from game_map import GameMap, MapTile


class LevelMap(GameMap):
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


class LevelTile(MapTile):
    def __init__(self, x, y, region):
        super().__init__(x, y, region, 0)