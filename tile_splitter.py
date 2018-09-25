import math
import pygame
import random


tile_variations_numbermap = {
    0: "corner_topleft", 1: "edge_top", 2: "corner_topright",
    3: "edge_left", 4: "fill", 5: "edge_right",
    6: "corner_bottomleft", 7: "edge_bottom", 8: "corner_bottomright"
}


def get_sheet_tiles(sheet_img, tile_ids):
    tile_surfaces = []
    for tile_id in tile_ids:
        tile_x = (tile_id % 13) * 4 + (tile_id % 13) * 32
        tile_y = math.floor(tile_id / 13) * 4 + math.floor(tile_id / 13) * 32
        tile_subsurface = sheet_img.subsurface((tile_x, tile_y, 32, 32))
        tile_surfaces.append(tile_subsurface)
    return tile_surfaces


def split_tile(sheet_img, distrib):
    tile_variations = {
        "edge_left": get_sheet_tiles(sheet_img, [0, 13, 26]),
        "edge_top": get_sheet_tiles(sheet_img, [1, 2, 3]),
        "edge_right": get_sheet_tiles(sheet_img, [4, 17, 30]),
        "edge_bottom": get_sheet_tiles(sheet_img, [27, 28, 29]),
        "fill": get_sheet_tiles(sheet_img, [14, 15, 16]),
        "corner_topleft": get_sheet_tiles(sheet_img, [39, 41, 43]),
        "corner_topright": get_sheet_tiles(sheet_img, [40, 42, 44]),
        "corner_bottomleft": get_sheet_tiles(sheet_img, [52, 54, 56]),
        "corner_bottomright": get_sheet_tiles(sheet_img, [53, 55, 57])
    }

    if type(distrib[0]) is int:
        distrib = [tile_variations_numbermap[i] for i in distrib]

    tile_surface = pygame.Surface((64, 64)).convert()
    tile_surface.set_colorkey((0, 0, 0))
    for i in range(9):
        piece_x = 16 * (i % 3)
        piece_y = 16 * math.floor(i / 3)
        tmp_variations = tile_variations[distrib[i]]
        tile_surface.blit(tmp_variations[random.randint(0, len(tmp_variations) - 1)], (piece_x, piece_y))
    return tile_surface