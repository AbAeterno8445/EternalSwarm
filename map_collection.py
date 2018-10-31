import pygame
import MGUI
import math


class MapCollection(MGUI.WidgetCollection):
    """
    Widget collection for game/level map.
    Handles mouse hovering over tiles and tile selection of given map object.
    """
    def __init__(self, x, y, width, height, map_obj):
        super().__init__()

        # Variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected_tile = None
        self.hovered = True

        self.add_widget(map_obj, "map", layer=-1)

        # Camera
        self.camera = MapCamera(0, 0)
        self.camera_drag = False
        self.center_camera()

        # Mouse-hover rectangle widget
        mouse_hover = MGUI.ImageWidget(0, 0, 48, 48)
        mouse_hover.set_border(True, (255, 255, 255))
        mouse_hover.set_visible(False)
        self.add_widget(mouse_hover, "mouse_hover", layer=1)

        # Selected tile widget
        selected_tile_widg = MGUI.ImageWidget(0, 0, 48, 48, "assets/UI/selected_tile.png")
        selected_tile_widg.set_border(True, (1, 1, 1))
        selected_tile_widg.set_visible(False)
        self.add_widget(selected_tile_widg, "selected_tile_widg", layer=2)

    def set_hovered(self, hovered):
        self.hovered = hovered

    def get_camera_position(self):
        return self.camera.get_position()

    def center_camera(self):
        if not self.camera_drag:
            sp_x, sp_y = self["map"].spawn_point
            cam_x = -sp_x * 48 + math.floor(self.width / 2) - 24
            cam_y = -sp_y * 48 + math.floor(self.height / 2) - 24
            self.camera.set_position(cam_x, cam_y)
            self["map"].set_position(*self.camera.get_position())

    def select_tile(self, tile_x, tile_y):
        self.selected_tile = self["map"].get_tile_at(tile_x, tile_y)

    def handle_event(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                # ESCAPE - Deselect tile
                if event.key == pygame.K_ESCAPE:
                    self.selected_tile = None
                # Selection movement via arrow keys
                elif event.key == pygame.K_LEFT:
                    if self.selected_tile and self.selected_tile.x > 0:
                        self.select_tile(self.selected_tile.x - 1, self.selected_tile.y)
                elif event.key == pygame.K_RIGHT:
                    if self.selected_tile and self.selected_tile.x < self["map"].width - 1:
                        self.select_tile(self.selected_tile.x + 1, self.selected_tile.y)
                elif event.key == pygame.K_UP:
                    if self.selected_tile and self.selected_tile.y > 0:
                        self.select_tile(self.selected_tile.x, self.selected_tile.y - 1)
                elif event.key == pygame.K_DOWN:
                    if self.selected_tile and self.selected_tile.y < self["map"].height - 1:
                        self.select_tile(self.selected_tile.x, self.selected_tile.y + 1)

            elif event.type in {pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP}:
                # Mouse related data
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_in_map = self["map"].get_bounds_at(self.x, self.y).collidepoint(mouse_x, mouse_y)
                if mouse_in_map:
                    tile_x = math.floor((mouse_x - self.x - self.camera.x - 8) / 48)
                    tile_y = math.floor((mouse_y - self.y - self.camera.y - 8) / 48)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # Select tile
                        if not self.camera_drag and self.hovered:
                            if mouse_in_map:
                                if 0 <= tile_x < self["map"].width and 0 <= tile_y < self["map"].height:
                                    self.select_tile(tile_x, tile_y)
                            else:
                                self.selected_tile = None

                elif event.type == pygame.MOUSEMOTION:
                    tmp_visible = True
                    # Mouseover rectangle
                    if self.hovered:
                        if mouse_in_map:
                            if 0 <= tile_x < self["map"].width and 0 <= tile_y < self["map"].height:
                                mh_x = tile_x * 48 + self.camera.x + 8
                                mh_y = tile_y * 48 + self.camera.y + 8
                                if not self["mouse_hover"].get_position() == (mh_x, mh_y):
                                    self["mouse_hover"].set_position(mh_x, mh_y)
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
                            self["map"].set_position(*self.camera.drag())
                    else:
                        tmp_visible = False
                    if self["mouse_hover"].is_visible() != tmp_visible:
                        self["mouse_hover"].set_visible(tmp_visible)
            # Stop camera drag
            if event.type == pygame.MOUSEBUTTONUP:
                self.camera_drag = False

    def update(self):
        # Selected tile info & overlay
        if self.selected_tile:
            if not self["selected_tile_widg"].is_visible():
                self["selected_tile_widg"].set_visible(True)
            selwidg_x = self.selected_tile.x * 48 + self.camera.x + 8
            selwidg_y = self.selected_tile.y * 48 + self.camera.y + 8
            if not self["selected_tile_widg"].get_position() == (selwidg_x, selwidg_y):
                self["selected_tile_widg"].set_position(selwidg_x, selwidg_y)
        else:
            if self["selected_tile_widg"].is_visible():
                self["selected_tile_widg"].set_visible(False)


class MapCamera(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.drag_x = 0
        self.drag_y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y

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