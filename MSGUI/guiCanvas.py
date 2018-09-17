import pygame
from .widget import Widget


default_backg_col = (0, 0, 0)
default_border_col = (255, 255, 255)


class GUICanvas(object):
    def __init__(self, x, y, width, height, bgcolor=default_backg_col):
        self.surface = pygame.Surface((width, height)).convert()

        self.x = x
        self.y = y

        self.backg_widget = Widget(0, 0, width, height)
        self.backg_widget.set_background(bgcolor)

        self.widgets_list = [self.backg_widget]
        self.sprite_list = pygame.sprite.LayeredDirty(self.backg_widget)
        self.sprite_list.change_layer(self.backg_widget, -1)

    def set_background(self, color):
        self.backg_widget.set_background(color)
        for widget in self.widgets_list:
            if widget.is_transparent():
                widget.set_background(color)

    # Element can be any pygame.sprite.DirtySprite object
    def add_element(self, element, layer=0, widget=False):
        if element not in self.sprite_list:
            self.sprite_list.add(element)
            self.sprite_list.change_layer(element, layer)
            if widget:
                if element.is_transparent():
                    element.set_background(self.backg_widget.get_background())
                self.widgets_list.append(element)

    def remove_element(self, element):
        if element in self.sprite_list:
            self.sprite_list.remove(element)
        if element in self.widgets_list:
            self.widgets_list.remove(element)

    def handle_event(self, event_list):
        for event in event_list:
            if event.type in {pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN}:
                mouse_pos = pygame.mouse.get_pos()
                event.pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)

            for widget in self.widgets_list:
                widget.handle_event(event)

    def draw(self, tgt_surface):
        upd_rects = []

        self.sprite_list.update()
        upd_rects += self.sprite_list.draw(self.surface)
        tgt_surface.blit(self.surface, (self.x, self.y))

        for i, rect in enumerate(upd_rects):
            upd_rects[i] = upd_rects[i].move(self.x, self.y)
        return upd_rects