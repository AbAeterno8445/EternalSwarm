import json
from game_map import GameMap, MapTile


class LevelMap(GameMap):
    def __init__(self, x, y, width, height, regions_json=None):
        super().__init__(x, y, width, height, regions_json)

        # List of buildings in level
        # Keys are building name and value is a list of coordinate tuples for each building of that type
        self.level_buildings = {}

    def load_level(self, region_name, level_id):
        region_name = region_name.lower()
        self.load_regions_json("levels/" + region_name + "/regions.json", False)
        lvl_path = "levels/" + region_name + "/level" + str(level_id)
        with open(lvl_path, "r") as file:
            level_data = json.loads(file.read())

            # Tile building codes
            tile_build_codes = level_data["building_codes"]

            # Load tiles & buildings
            tmp_mapdata = level_data["map_data"]

            self.height = len(tmp_mapdata)
            # Turn strings into lists
            for i in range(self.height):
                tmp_mapdata[i] = [t.strip() for t in tmp_mapdata[i].split(',')]

            self.width = len(tmp_mapdata[0])

            self.map_data.clear()
            self.level_buildings.clear()
            for i in range(self.height):
                self.map_data.append([])
                for j in range(self.width):
                    tile_data = tmp_mapdata[i][j].split(':')
                    # Base tile
                    region = self.regions[int(tile_data[0])]
                    tmp_tile = MapTile(j, i, region)
                    self.map_data[i].append(tmp_tile)
                    # Extra tile flags
                    if len(tile_data) > 1:
                        for flag in tile_data[1:]:
                            if flag == "o":  # Tile owned by player
                                tmp_tile.owned = True
                            elif flag in tile_build_codes:  # Building in tile
                                bname = tile_build_codes[flag]
                                if bname not in self.level_buildings:
                                    self.level_buildings[bname] = []
                                self.level_buildings[bname].append((j, i, tmp_tile.owned))

        self.update_tilemap()