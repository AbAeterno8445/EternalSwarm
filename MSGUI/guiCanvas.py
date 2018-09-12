import pygame


default_backg_col = (0, 0, 0)
default_border_col = (255, 255, 255)


class GUICanvas(pygame.Surface):
    def __init__(self, x, y, width, height):
        super(GUICanvas, self).__init__((width, height), pygame.SRCALPHA)

        self.widgets_list = []
        self.sprite_list = pygame.sprite.LayeredDirty()

        self.fill(default_backg_col)
        self.background = pygame.Surface((width, height))
        self.background.convert()
        self.background.fill(default_backg_col)

        self.sprite_list.clear(self, self.background)

        self.x = x
        self.y = y
        self.border = 0
        self.border_color = default_border_col

    def set_background_color(self, color):
        self.fill(color)
        self.background.fill(color)
        self.sprite_list.clear(self, self.background)

    def set_border(self, border, color=default_border_col):
        self.border = border
        self.border_color = color

    def add_element(self, element, layer=0, widget=False):
        self.sprite_list.add(element)
        self.sprite_list.change_layer(element, layer)
        if widget:
            self.widgets_list.append(element)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            event.pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)

        for widget in self.widgets_list:
            widget.update(event)

    def draw(self, tgt_surface):
        self.sprite_list.update()
        self.sprite_list.draw(self)

        tgt_surface.blit(self, (self.x, self.y))
        if self.border > 0:
            pygame.draw.rect(tgt_surface, self.border_color,
                             (self.x, self.y, self.get_width(), self.get_height()), self.border)