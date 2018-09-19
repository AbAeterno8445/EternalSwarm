import pygame
import MSGUI
from mapTile import MapTile
from random import randint


class GameMap(MSGUI.Widget):
    def __init__(self, x, y, width, height, regions=None):
        widget_width = 16 + width * 48
        widget_height = 16 + height * 48
        super(GameMap, self).__init__(x, y, widget_width, widget_height)
        self.set_transparent(True)

        self.width = width
        self.height = height

        self.tilelist = pygame.sprite.LayeredDirty()
        self.tilemap_surface = pygame.Surface(self.get_size()).convert()
        self.tilemap_surface.set_colorkey((0, 0, 0))

        self.map_data = []
        self.regions = []
        if regions:
            self.add_region_multiple(regions)

    # Add a region to the map, rarity is 0-100 chance to spawn
    def add_region(self, name, reg_image, gen=True):
        self.regions.append(MapRegion(name, reg_image))
        if gen:
            self.generate_tilemap()

    # Add multiple regions, regions is a list of tuples (name, img, rarity)
    def add_region_multiple(self, regions):
        for reg in regions:
            self.add_region(*reg, gen=False)
        self.generate_tilemap()

    def generate_tilemap(self):
        self.map_data.clear()

        regions_len = len(self.regions) - 1
        for i in range(self.height):
            self.map_data.append([])
            for j in range(self.width):
                self.map_data[i].append(randint(0, regions_len))
        self.update_tilemap()

    def update_tilemap(self):
        for i in range(self.height):
            for j in range(self.width):
                cur_tile_id = self.map_data[i][j]
                tile_x = j * 48
                tile_y = i * 48
                tmp_tile = MapTile(tile_x, tile_y, 64, 64, self.regions[cur_tile_id].img)

                neighbor_top = False
                if i > 0:
                    if self.map_data[i - 1][j] == cur_tile_id:
                        neighbor_top = True

                neighbor_bottom = False
                if i < self.height - 1:
                    if self.map_data[i + 1][j] == cur_tile_id:
                        neighbor_bottom = True

                neighbor_left = False
                if j > 0:
                    if self.map_data[i][j - 1] == cur_tile_id:
                        neighbor_left = True

                neighbor_right = False
                if j < self.width - 1:
                    if self.map_data[i][j + 1] == cur_tile_id:
                        neighbor_right = True

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

                tmp_tile.set_distribution(tile_distrib)
                self.tilelist.add(tmp_tile)
                self.tilelist.change_layer(tmp_tile, -self.map_data[i][j])
        self.tilelist.update()
        self.tilelist.draw(self.tilemap_surface)

    def _get_appearance(self, *args):
        return self.tilemap_surface


class MapRegion(object):
    def __init__(self, name, img):
        self.name = name
        self.img = img