import pygame
import MSGUI
import math
from game_map import GameMap


class CanvasTerrain(MSGUI.GUICanvas):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (0, 110, 110))

        self.backg_widget.set_border(True, (0, 150, 150))

        self.gamemap = GameMap(0, 0, 24, 24)
        self.gamemap.load_regions_json("assets/map_regions.json")
        self.add_element(self.gamemap)

        self.camera = MapCamera(*self.gamemap.get_position())
        self.camera_drag = False

        self.mouse_hover = MSGUI.ImageWidget(0, 0, 48, 48)
        self.mouse_hover.set_border(True, (255, 255, 255))
        self.add_element(self.mouse_hover)

        self.label_tileinfo = MSGUI.Label(8, 8, 200, 22, pygame.font.Font("assets/Dosis.otf", 18))
        self.label_tileinfo.set_background(self.backg_widget.get_background())
        self.label_tileinfo.set_border(True, self.backg_widget.get_border_color())
        self.add_element(self.label_tileinfo)

    def handle_event(self, event_list):
        super().handle_event(event_list)

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.gamemap.generate_tilemap()

            # Stop camera drag
            if event.type == pygame.MOUSEBUTTONUP:
                self.camera_drag = False

            if self.focus_hovered:
                if event.type == pygame.MOUSEMOTION:
                    # Mouseover info
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.gamemap.get_bounds().move(self.x, self.y).collidepoint(mouse_x, mouse_y):
                        tile_x = math.floor((mouse_x - self.x - self.camera.x - 8) / 48)
                        tile_y = math.floor((mouse_y - self.y - self.camera.y - 8) / 48)
                        if 0 <= tile_x < self.gamemap.width and 0 <= tile_y < self.gamemap.height:
                            mh_x = tile_x * 48 + self.camera.x + 8
                            mh_y = tile_y * 48 + self.camera.y + 8
                            self.mouse_hover.set_position(mh_x, mh_y)
                            if not self.mouse_hover.is_visible():
                                self.mouse_hover.set_visible(True)

                            self.label_tileinfo.set_text(self.gamemap.get_region_at(tile_x, tile_y).name)
                        else:
                            self.mouse_hover.set_visible(False)
                    else:
                        self.mouse_hover.set_visible(False)

                    # Camera dragging
                    if not self.camera_drag:
                        if event.buttons[0]:
                            self.camera_drag = True
                            self.camera.begin_drag()
                    else:
                        self.gamemap.set_position(*self.camera.drag())


class MapCamera(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.drag_x = 0
        self.drag_y = 0

    def get_position(self):
        return (self.x, self.y)

    def begin_drag(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.drag_x = self.x - mouse_x
        self.drag_y = self.y - mouse_y

    def drag(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x + self.drag_x
        self.y = mouse_y + self.drag_y
        return self.get_position()