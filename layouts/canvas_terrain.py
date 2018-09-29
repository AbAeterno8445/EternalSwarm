import pygame
import MSGUI
from game_map import GameMap
from map_collection import MapCollection
from .cv_terrain_levelinfo import TerrainLevelinfo


class CanvasTerrain(MSGUI.GUICanvas):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (0, 110, 110))

        # Variables
        self.start_game = False  # Set to true to begin game using selected tile data

        self.backg_widget.set_border(True, (0, 150, 150))

        self.gamemap = GameMap(0, 0, 32, 32, "assets/map_regions.json")
        self.map_collection = MapCollection(x, y, width, height, self.gamemap)
        self.add_element(self.map_collection.get_widgets_list())

        # Tile level information widget
        self.panel_tileinfo = TerrainLevelinfo(4, 4, 150, 200)
        self.panel_tileinfo["capture_button"].set_callback(self.capture_click)
        self.panel_tileinfo.set_visible(False)
        self.add_element(self.panel_tileinfo.get_widgets_list())

    def capture_click(self):
        self.start_game = True

    def handle_event(self, event_list):
        super().handle_event(event_list)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        info_hovered = self.panel_tileinfo.is_visible() and \
                       self.panel_tileinfo["background"].get_bounds_at(self.x, self.y).collidepoint(mouse_x, mouse_y)

        if not info_hovered and self.focus_hovered:
            self.map_collection.set_hovered(True)
        else:
            self.map_collection.set_hovered(False)

        self.map_collection.handle_event(event_list)
        self.map_collection.update()

    def draw(self, tgt_surface):
        sel_tile = self.map_collection.selected_tile
        if sel_tile:
            if not self.panel_tileinfo.is_visible():
                self.panel_tileinfo.set_visible(True)
            self.panel_tileinfo.update_data(sel_tile)
        else:
            if self.panel_tileinfo.is_visible():
                self.panel_tileinfo.set_visible(False)

        return super().draw(tgt_surface)