import pygame


default_backg_col = (0, 0, 0)
default_border_col = (255, 255, 255)


class GUICanvas(pygame.Surface):
    def __init__(self, x, y, width, height):
        super(GUICanvas, self).__init__((width, height), pygame.SRCALPHA)

        self.gui_widgets_list = pygame.sprite.LayeredDirty()
        self.sprite_list = pygame.sprite.LayeredDirty()

        self.x = x
        self.y = y

        self.fill(default_backg_col)
        self.background = pygame.Surface((width, height))
        self.background.convert()
        self.background.fill(default_backg_col)

        self.border = 0
        self.border_color = default_border_col

        self.sprite_list.clear(self, self.background)

    def set_background_color(self, color):
        self.fill(color)
        self.background.fill(color)
        self.sprite_list.clear(self, self.background)

    def set_border(self, border, color=default_border_col):
        self.border = border
        self.border_color = color

    def add_widget(self, widget, layer=0):
        self.gui_widgets_list.add(widget)
        self.gui_widgets_list.change_layer(widget, layer)

    def add_sprite(self, spr, layer=0):
        self.sprite_list.add(spr)
        self.sprite_list.change_layer(spr, layer)

    def handle_event(self, event):
        try:
            event.pos = (event.pos[0] - self.x, event.pos[1] - self.y)
        except AttributeError:
            pass
        self.gui_widgets_list.update(event)

    def draw(self, tgt_surface):
        self.sprite_list.update()
        self.sprite_list.draw(self)

        self.gui_widgets_list.draw(self)

        tgt_surface.blit(self, (self.x, self.y))
        if self.border > 0:
            pygame.draw.rect(tgt_surface, self.border_color,
                             (self.x, self.y, self.get_width(), self.get_height()), self.border)