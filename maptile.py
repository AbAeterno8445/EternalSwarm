import pygame
import MSGUI
import math
import random


class MapTile(MSGUI.ImageWidget):
    def __init__(self, x, y, width, height, icon=None):
        self.tile_variations = {
            "edge_left": [],
            "edge_top": [],
            "edge_right": [],
            "edge_bottom": [],
            "fill": [],
            "corner_topleft": [],
            "corner_topright": [],
            "corner_bottomleft": [],
            "corner_bottomright": []
        }

        self.tile_variations_numbermap = {
            0: "corner_topleft", 1: "edge_top", 2: "corner_topright",
            3: "edge_left", 4: "fill", 5: "edge_right",
            6: "corner_bottomleft", 7: "edge_bottom", 8: "corner_bottomright"
        }

        self.tile_distrib = [
            "corner_topleft", "edge_top", "corner_topright",
            "edge_left", "fill", "edge_right",
            "corner_bottomleft", "edge_bottom", "corner_bottomright"
        ]

        super().__init__(x, y, width, height, icon)

    def _get_sheet_tiles(self, *args):
        tile_surfaces = []
        for tile_id in args:
            tile_x = (tile_id % 13) * 4 + (tile_id % 13) * 32
            tile_y = math.floor(tile_id / 13) * 4 + math.floor(tile_id / 13) * 32
            tile_subsurface = self._icon.subsurface((tile_x, tile_y, 32, 32))
            tile_surfaces.append(tile_subsurface)
        return tile_surfaces

    # Receives tile sheet as icon
    def set_icon(self, icon):
        super().set_icon(icon)

        # Load necessary tiles from the provided sheet
        self.tile_variations["edge_left"] = self._get_sheet_tiles(0, 13, 26)
        self.tile_variations["edge_top"] = self._get_sheet_tiles(1, 2, 3)
        self.tile_variations["edge_right"] = self._get_sheet_tiles(4, 17, 30)
        self.tile_variations["edge_bottom"] = self._get_sheet_tiles(27, 28, 29)
        self.tile_variations["fill"] = self._get_sheet_tiles(14, 15, 16)
        self.tile_variations["corner_topleft"] = self._get_sheet_tiles(39, 41, 43)
        self.tile_variations["corner_topright"] = self._get_sheet_tiles(40, 42, 44)
        self.tile_variations["corner_bottomleft"] = self._get_sheet_tiles(52, 54, 56)
        self.tile_variations["corner_bottomright"] = self._get_sheet_tiles(53, 55, 57)

    # Sets the distribution of tile-pieces for the tile
    # Distrib is an array of 9 elements detailing what kind of piece goes in each position
    def set_distribution(self, distrib):
        if type(distrib[0]) is int:
            distrib = [self.tile_variations_numbermap[i] for i in distrib]
        self.tile_distrib = distrib

    def _get_appearance(self, *args):
        icon_surface = super()._get_appearance(*args)
        icon_surface.set_colorkey((0, 0, 0))

        for i in range(9):
            piece_x = 16 * (i % 3)
            piece_y = 16 * math.floor(i / 3)
            icon_surface.blit(self.tile_variations[self.tile_distrib[i]][random.randint(0, 2)], (piece_x, piece_y))
        # pygame.draw.rect(icon_surface, (255, 255, 255), (8, 8, 48, 48), 1)

        return icon_surface