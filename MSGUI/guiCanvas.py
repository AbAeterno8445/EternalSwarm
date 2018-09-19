import pygame
from .imageWidget import ImageWidget


default_backg_col = (0, 0, 0)
default_border_col = (255, 255, 255)


class GUICanvas(object):
    def __init__(self, x, y, width, height, bgcolor=default_backg_col):
        self.surface = pygame.Surface((width, height)).convert()

        self.x = x
        self.y = y

        self.focus_hovered = False
        self.focus_clicked = False

        self.backg_widget = ImageWidget(0, 0, width, height)
        self.backg_widget.set_transparent(False)
        self.backg_widget.set_background(bgcolor)

        self.widgets_dict = {"background": self.backg_widget}
        self.sprite_list = pygame.sprite.LayeredDirty(self.backg_widget)
        self.sprite_list.change_layer(self.backg_widget, -1)

    def is_hovered(self):
        return self.focus_hovered

    def is_focused(self):
        return self.focus_clicked

    def set_background(self, color):
        self.backg_widget.set_background(color)
        for widget in self.widgets_dict:
            if self.widgets_dict[widget].is_transparent():
                self.widgets_dict[widget].set_background(color)

    # Element can be any pygame.sprite.DirtySprite object
    def add_element(self, element, layer=0, widget=None):
        if widget and widget in self.widgets_dict:
            raise Exception("Widget with that name already exists! (%s)" % widget)

        if element not in self.sprite_list:
            self.sprite_list.add(element)
            self.sprite_list.change_layer(element, layer)
            if widget:
                if element.is_transparent():
                    element.set_background(self.backg_widget.get_background())
                self.widgets_dict[widget] = element

    def remove_element(self, element):
        if element in self.sprite_list:
            self.sprite_list.remove(element)
        if element in self.widgets_dict:
            self.widgets_dict.pop(element)

    def get_widget(self, widget_name):
        try:
            return self.widgets_dict[widget_name]
        except KeyError:
            return None

    def handle_event(self, event_list):
        for event in event_list:
            if event.type in {pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN}:
                mouse_pos = pygame.mouse.get_pos()
                event.pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)

                if event.type == pygame.MOUSEMOTION:
                    if self.backg_widget.rect.collidepoint(event.pos):
                        self.focus_hovered = True
                    else:
                        self.focus_hovered = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.backg_widget.rect.collidepoint(event.pos):
                        if event.button in (1, 2, 3):
                            self.focus_clicked = True
                    else:
                        self.focus_clicked = False

            for widget in self.widgets_dict:
                self.widgets_dict[widget].handle_event(event)

    def draw(self, tgt_surface):
        upd_rects = []

        self.sprite_list.update()
        upd_rects += self.sprite_list.draw(self.surface)
        tgt_surface.blit(self.surface, (self.x, self.y))

        for rect in upd_rects:
            rect.move_ip(self.x, self.y)
        return upd_rects