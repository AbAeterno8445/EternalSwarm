import pygame
from .image_widget import ImageWidget
from .widget import Widget


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

        self.widgets_list = []
        self.sprite_list = pygame.sprite.LayeredDirty(self.backg_widget)
        self.sprite_list.change_layer(self.backg_widget, -1)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def is_hovered(self):
        return self.focus_hovered

    def is_focused(self):
        return self.focus_clicked

    def get_width(self):
        return self.backg_widget.get_size()[0]

    def get_height(self):
        return self.backg_widget.get_size()[1]

    def get_size(self):
        return self.backg_widget.get_size()

    def set_background(self, color):
        self.backg_widget.set_background(color)
        for widget in self.widgets_list:
            if widget.is_transparent():
                widget.set_background(color)

    # Element can be any pygame.sprite.DirtySprite object
    # Element can also be a list of tuples (element, layer)
    # Objects inherited from Widget class get event handling
    def add_element(self, element, layer=0):
        if type(element) is list:
            for e in element:
                self.add_element(e[0], e[1])
            return

        if element not in self.sprite_list:
            self.sprite_list.add(element)
            self.sprite_list.change_layer(element, layer)
            if isinstance(element, Widget):
                self.widgets_list.append(element)
                if element.is_transparent():
                    element.set_background(self.backg_widget.get_background())

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

            for widget in self.widgets_list:
                widget.handle_event(event)

    def draw(self, tgt_surface):
        # Transparency
        if self.backg_widget.is_transparent() and not self.surface.get_colorkey() == self.backg_widget.get_background():
            self.surface.set_colorkey(self.backg_widget.get_background())

        self.sprite_list.update()
        upd_rects = self.sprite_list.draw(self.surface)
        if len(upd_rects) > 0:
            tgt_surface.blit(self.surface, self.get_position())

            for rect in upd_rects:
                rect.move_ip(self.x, self.y)
        return upd_rects