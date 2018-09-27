import pygame
import MSGUI
import math
from game_map import GameMap
from .sub_terrain_levelinfo import TerrainLevelinfo


class CanvasTerrain(MSGUI.GUICanvas):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (0, 110, 110))

        # Variables
        self.selected_tile = None
        self.start_game = False  # Set to true to begin game using selected tile data

        self.backg_widget.set_border(True, (0, 150, 150))

        self.gamemap = GameMap(0, 0, 32, 32, "assets/map_regions.json")
        self.add_element(self.gamemap)

        sp_x, sp_y = self.gamemap.spawn_point
        cam_x = -sp_x * 48 + math.floor(self.get_width() / 2) - 24
        cam_y = -sp_y * 48 + math.floor(self.get_height() / 2) - 24
        self.camera = MapCamera(cam_x, cam_y)
        self.camera_drag = False

        self.mouse_hover = MSGUI.ImageWidget(0, 0, 48, 48)
        self.mouse_hover.set_border(True, (255, 255, 255))
        self.add_element(self.mouse_hover)

        self.selected_tile_widg = MSGUI.ImageWidget(0, 0, 48, 48, "assets/selected_tile.png")
        self.selected_tile_widg.set_visible(False)
        self.add_element(self.selected_tile_widg)

        # Tile level information widget
        self.panel_tileinfo = TerrainLevelinfo(4, 4, 150, 200)
        self.panel_tileinfo["capture_button"].set_callback(self.capture_click)
        self.panel_tileinfo.set_visible(False)
        self.add_element(self.panel_tileinfo.get_widgets_list())

        self.gamemap.set_position(*self.camera.get_position())

    def capture_click(self):
        self.start_game = True

    def handle_event(self, event_list):
        super().handle_event(event_list)

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.gamemap.generate_tilemap()

            if self.focus_hovered:
                if event.type == pygame.KEYDOWN:
                    # ESCAPE - Hide tile info screen
                    if event.key == pygame.K_ESCAPE:
                        self.selected_tile = None

                elif event.type in {pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP}:
                    # Mouse related data
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_inside = self.gamemap.get_bounds().move(self.x, self.y).collidepoint(mouse_x, mouse_y)
                    if mouse_inside:
                        tile_x = math.floor((mouse_x - self.x - self.camera.x - 8) / 48)
                        tile_y = math.floor((mouse_y - self.y - self.camera.y - 8) / 48)
                    info_hovered = self.panel_tileinfo.is_visible() and \
                                   self.panel_tileinfo["background"].get_bounds_at(self.x, self.y).collidepoint(mouse_x, mouse_y)

                    if event.type == pygame.MOUSEBUTTONUP:
                        # Select tile
                        if not self.camera_drag:
                            if not info_hovered:
                                if mouse_inside:
                                    if 0 <= tile_x < self.gamemap.width and 0 <= tile_y < self.gamemap.height:
                                        self.selected_tile = self.gamemap.get_tile_at(tile_x, tile_y)
                                        self.panel_tileinfo.update_data(self.selected_tile)
                                else:
                                    self.selected_tile = None

                    elif event.type == pygame.MOUSEMOTION:
                        tmp_visible = True
                        # Mouseover rectangle
                        if not info_hovered:
                            if mouse_inside:
                                if 0 <= tile_x < self.gamemap.width and 0 <= tile_y < self.gamemap.height:
                                    mh_x = tile_x * 48 + self.camera.x + 8
                                    mh_y = tile_y * 48 + self.camera.y + 8
                                    self.mouse_hover.set_position(mh_x, mh_y)
                                    if not self.mouse_hover.is_visible():
                                        self.mouse_hover.set_visible(True)
                                else:
                                    tmp_visible = False
                            else:
                                tmp_visible = False

                            # Camera dragging
                            if not self.camera_drag:
                                if event.buttons[0]:
                                    self.camera_drag = True
                                    self.camera.begin_drag()
                            else:
                                self.gamemap.set_position(*self.camera.drag())
                        else:
                            tmp_visible = False
                        if self.mouse_hover.is_visible() != tmp_visible:
                            self.mouse_hover.set_visible(tmp_visible)
            # Stop camera drag
            if event.type == pygame.MOUSEBUTTONUP:
                self.camera_drag = False

    def draw(self, tgt_surface):
        # Selected tile info & overlay
        if self.selected_tile:
            if not self.panel_tileinfo.is_visible():
                self.panel_tileinfo.set_visible(True)
            if not self.selected_tile_widg.is_visible():
                self.selected_tile_widg.set_visible(True)
            selwidg_x = self.selected_tile.x * 48 + self.camera.x + 8
            selwidg_y = self.selected_tile.y * 48 + self.camera.y + 8
            if not self.selected_tile_widg.get_position() == (selwidg_x, selwidg_y):
                self.selected_tile_widg.set_position(selwidg_x, selwidg_y)
        else:
            if self.panel_tileinfo.is_visible():
                self.panel_tileinfo.set_visible(False)
            if self.selected_tile_widg.is_visible():
                self.selected_tile_widg.set_visible(False)

        return super().draw(tgt_surface)


class MapCamera(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.drag_x = 0
        self.drag_y = 0

    def get_position(self):
        return self.x, self.y

    def begin_drag(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.drag_x = self.x - mouse_x
        self.drag_y = self.y - mouse_y

    def drag(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x + self.drag_x
        self.y = mouse_y + self.drag_y
        return self.get_position()