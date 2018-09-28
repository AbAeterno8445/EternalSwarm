import pygame
import json
import math
import os
import MSGUI
from tile_splitter import split_tile
from random import randint


class GameMap(MSGUI.Widget):
    def __init__(self, x, y, width, height, regions_json=None):
        super().__init__(x, y, width, height)
        self.set_map_size(width, height)
        self.set_transparent(True)

        self.width = width
        self.height = height

        self.tilelist = pygame.sprite.LayeredDirty()
        self.tilemap_surface = pygame.Surface(self.get_size()).convert()
        self.tilemap_surface.set_colorkey((0, 0, 0))

        self.spawn_point = (math.floor((width + randint(0, 1)) / 2), math.floor((height + randint(0, 1)) / 2))
        self.map_data = []  # 2d list of ints - each int is the regions list index # for that tile
        self.regions = []
        if regions_json:
            self.load_regions_json(regions_json)

    # Width, height in tiles, automatically adapts bounds size
    def set_map_size(self, width, height):
        self.width = width
        self.height = height
        widget_width = 16 + width * 48
        widget_height = 16 + height * 48
        super().set_bounds_size(widget_width, widget_height)

    def load_regions_json(self, json_path, gen_map=True):
        with open(json_path, "r") as json_file:
            loaded_regions = json.loads(json_file.read())

        self.regions.clear()
        for reg in loaded_regions:
            tmp_img = pygame.image.load("assets/regions/" + reg["img_path"])
            tmp_region = MapRegion(reg["name"], tmp_img)

            region_attr = ["spawn_dist", "max_size", "decor", "decor_density", "freq", "expansion"]
            for attr in region_attr:
                if attr in reg:
                    if attr == "decor":  # Preemptively load decor images
                        tmp_region.decor = [pygame.image.load("assets/regions/decor/" + img) for img in reg[attr]]
                    else:
                        tmp_region.__setattr__(attr, reg[attr])

            self.regions.append(tmp_region)

        if gen_map:
            self.generate_tilemap()

    def get_tile_at(self, x, y):
        return self.map_data[y][x]

    @staticmethod
    def get_tile_distance(tile_start, tile_end):
        dist = abs(tile_start[0] - tile_end[0]) + abs(tile_start[1] - tile_end[1])
        return dist

    def _generate_region_at(self, region, start_x, start_y):
        if self.get_tile_distance(self.spawn_point, (start_x, start_y)) < region.spawn_dist:
            return False

        created = 0
        create_chance = max(5, region.expansion)
        created_tiles = [(start_x, start_y)]
        closed_tiles = []

        while len(created_tiles) > 0:
            cur_tile = created_tiles[0]
            closed_tiles.append(cur_tile)

            x, y = cur_tile
            self.map_data[y][x].region = region
            created += 1
            if created >= region.max_size:
                break

            neighbors = []
            for tile in closed_tiles + created_tiles:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 or j == 0 and not (i == 0 and j == 0):
                            nx, ny = tile[0] + i, tile[1] + j
                            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in closed_tiles:
                                if self.get_tile_distance((nx, ny), self.spawn_point) > region.spawn_dist and self.map_data[ny][nx].region == self.regions[0]:
                                    neighbors.append((nx, ny))

            for n_tile in neighbors:
                if randint(1, 101) <= create_chance:
                    created_tiles.append(n_tile)
                    break
            created_tiles.remove(cur_tile)

        return True

    def generate_tilemap(self):
        if len(self.regions) == 0:
            return
        self.map_data.clear()

        # Create tile instances
        for i in range(self.height):
            self.map_data.append([])
            for j in range(self.width):
                if self.spawn_point == (j, i):
                    tile_diff = 1
                else:
                    tile_diff = 1 + math.floor(self.get_tile_distance(self.spawn_point, (j, i)) / 6) + randint(0, 2)
                tmp_tile = MapTile(j, i, self.regions[0], tile_diff)

                self.map_data[i].append(tmp_tile)

        # Create regions
        if len(self.regions) > 1:
            for i in range(self.height):
                for j in range(self.width):
                    if self.map_data[j][i].region == self.regions[0]:
                        picked_region = randint(1, len(self.regions) - 1)
                        if randint(0, 100) < self.regions[picked_region].freq:
                            self._generate_region_at(self.regions[picked_region], j, i)

        # Set spawn point as owned by player
        self.get_tile_at(*self.spawn_point).owned = True

        # Assign levels to tiles based on region
        for i in range(self.height):
            for j in range(self.width):
                cur_tile = self.map_data[j][i]
                cur_region = cur_tile.region
                level_path = "levels/" + cur_region.name.lower() + "/"
                try:
                    levels_list = os.listdir(level_path)
                except FileNotFoundError:
                    continue
                if "regions.json" in levels_list:
                    levels_list.remove("regions.json")

                cur_tile.level_id = randint(1, len(levels_list))

        self.update_tilemap()

    def update_tilemap(self):
        self.tilemap_surface.fill((0, 0, 0))
        self.tilelist.empty()
        for i in range(self.height):
            for j in range(self.width):
                cur_tile = self.map_data[i][j]
                cur_region = cur_tile.region
                tile_x = j * 48
                tile_y = i * 48

                # Tile neighbors - checks region, owned and capturable
                neighbor_top = False
                neighbor_top_owned = False
                if i > 0:
                    neighbor = self.map_data[i - 1][j]
                    if neighbor.region == cur_tile.region:
                        neighbor_top = True
                    neighbor_top_owned = neighbor.owned
                    if cur_tile.owned:
                        neighbor.capturable = True

                neighbor_bottom = False
                neighbor_bottom_owned = False
                if i < self.height - 1:
                    neighbor = self.map_data[i + 1][j]
                    if neighbor.region == cur_tile.region:
                        neighbor_bottom = True
                    neighbor_bottom_owned = neighbor.owned
                    if cur_tile.owned:
                        neighbor.capturable = True

                neighbor_left = False
                neighbor_left_owned = False
                if j > 0:
                    neighbor = self.map_data[i][j - 1]
                    if neighbor.region == cur_tile.region:
                        neighbor_left = True
                    neighbor_left_owned = neighbor.owned
                    if cur_tile.owned:
                        neighbor.capturable = True

                neighbor_right = False
                neighbor_right_owned = False
                if j < self.width - 1:
                    neighbor = self.map_data[i][j + 1]
                    if neighbor.region == cur_tile.region:
                        neighbor_right = True
                    neighbor_right_owned = neighbor.owned
                    if cur_tile.owned:
                        neighbor.capturable = True

                # Tile piece distribution based on neighbors
                tile_distrib = []

                # Top-left piece
                if neighbor_top and neighbor_left:
                    tile_distrib.append("fill")
                elif neighbor_top and not neighbor_left:
                    tile_distrib.append("edge_left")
                elif not neighbor_top and neighbor_left:
                    tile_distrib.append("edge_top")
                else:
                    tile_distrib.append("corner_topleft")

                # Top piece
                if neighbor_top:
                    tile_distrib.append("fill")
                else:
                    tile_distrib.append("edge_top")

                # Top-right piece
                if neighbor_top and neighbor_right:
                    tile_distrib.append("fill")
                elif neighbor_top and not neighbor_right:
                    tile_distrib.append("edge_right")
                elif not neighbor_top and neighbor_right:
                    tile_distrib.append("edge_top")
                else:
                    tile_distrib.append("corner_topright")

                # Left piece
                if neighbor_left:
                    tile_distrib.append("fill")
                else:
                    tile_distrib.append("edge_left")

                # Middle piece
                tile_distrib.append("fill")

                # Right piece
                if neighbor_right:
                    tile_distrib.append("fill")
                else:
                    tile_distrib.append("edge_right")

                # Bottom-left piece
                if neighbor_bottom and neighbor_left:
                    tile_distrib.append("fill")
                elif neighbor_bottom and not neighbor_left:
                    tile_distrib.append("edge_left")
                elif not neighbor_bottom and neighbor_left:
                    tile_distrib.append("edge_bottom")
                else:
                    tile_distrib.append("corner_bottomleft")

                # Bottom piece
                if neighbor_bottom:
                    tile_distrib.append("fill")
                else:
                    tile_distrib.append("edge_bottom")

                # Bottom-right piece
                if neighbor_bottom and neighbor_right:
                    tile_distrib.append("fill")
                elif neighbor_bottom and not neighbor_right:
                    tile_distrib.append("edge_right")
                elif not neighbor_bottom and neighbor_right:
                    tile_distrib.append("edge_bottom")
                else:
                    tile_distrib.append("corner_bottomright")

                tmp_tile_sprite = pygame.sprite.DirtySprite(self.tilelist)
                tmp_tile_sprite.image = split_tile(cur_region.img, tile_distrib)
                tmp_tile_sprite.rect = tmp_tile_sprite.image.get_rect(topleft=(tile_x, tile_y))
                self.tilelist.change_layer(tmp_tile_sprite, -self.regions.index(cur_region))

                # Owned tile overlay
                if cur_tile.owned:
                    tmp_owned_sprite = pygame.sprite.DirtySprite(self.tilelist)
                    tmp_owned_sprite.image = pygame.Surface((50, 50)).convert()
                    tmp_owned_sprite.image.set_colorkey((0, 0, 0))
                    # Draw edges based on neighbors
                    if not neighbor_top_owned:
                        pygame.draw.line(tmp_owned_sprite.image, (255, 255, 255), (0, 0), (46, 0), 2)
                        pygame.draw.line(tmp_owned_sprite.image, (255, 255, 115), (0, 0), (46, 0), 1)
                    if not neighbor_right_owned:
                        pygame.draw.line(tmp_owned_sprite.image, (255, 255, 255), (46, 0), (46, 46), 2)
                        pygame.draw.line(tmp_owned_sprite.image, (255, 255, 115), (46, 0), (46, 46), 1)
                    if not neighbor_left_owned:
                        pygame.draw.line(tmp_owned_sprite.image, (255, 255, 255), (0, 0), (0, 46), 2)
                        pygame.draw.line(tmp_owned_sprite.image, (255, 255, 115), (0, 0), (0, 46), 1)
                    if not neighbor_bottom_owned:
                        pygame.draw.line(tmp_owned_sprite.image, (255, 255, 255), (0, 46), (46, 46), 2)
                        pygame.draw.line(tmp_owned_sprite.image, (255, 255, 115), (0, 46), (46, 46), 1)

                    tmp_owned_sprite.rect = tmp_owned_sprite.image.get_rect(topleft=(tile_x + 8, tile_y + 8))
                    self.tilelist.change_layer(tmp_owned_sprite, 10)

                # Decor images
                if len(cur_region.decor) > 0:
                    for k in range(randint(1 + cur_region.decor_density, 4 + cur_region.decor_density)):
                        img = cur_region.decor[randint(0, len(cur_region.decor) - 1)]
                        tmp_decor = pygame.sprite.DirtySprite(self.tilelist)
                        self.tilelist.change_layer(tmp_decor, 5)
                        tmp_decor.image = img.copy()
                        d_x = tile_x + 8 + randint(0, 25) + randint(0, 25)
                        d_y = tile_y + 8 + randint(0, 21) + randint(0, 21)
                        tmp_decor.rect = tmp_decor.image.get_rect(center=(d_x, d_y))

        self.tilelist.update()
        self.tilelist.draw(self.tilemap_surface)
        self.mark_dirty()

    def _get_appearance(self, *args):
        return self.tilemap_surface


class MapRegion(object):
    def __init__(self, name, img):
        self.name = name
        self.img = img
        self.spawn_dist = 0  # Distance from spawnpoint, used in generation
        self.max_size = 1
        self.decor = []
        self.decor_density = 2
        self.freq = 100
        self.expansion = 33


class MapTile(object):
    def __init__(self, x, y, region, difficulty=1):
        self.x = x
        self.y = y
        self.region = region
        self.difficulty = difficulty
        self.owned = False
        self.capturable = False
        self.level_id = 1