import pygame


default_backg_col = (0, 0, 0)


class GUICanvas(pygame.Surface):
    def __init__(self, x, y, width, height):
        super(GUICanvas, self).__init__((width, height), pygame.SRCALPHA)

        self.sprite_list = pygame.sprite.LayeredDirty()

        self.x = x
        self.y = y

        self.fill(default_backg_col)
        self.background = pygame.Surface((width, height))
        self.background.convert()
        self.background.fill(default_backg_col)

        self.sprite_list.clear(self, self.background)

    def set_background_color(self, color):
        """
        Sets the background color for this canvas
        parameters:     tuple with 3 variables (r, g, b)
        return values:  -
        """
        self.fill(color)
        self.background.fill(color)
        self.sprite_list.clear(self, self.background)

    def add_element(self, spr):
        """
        Adds a gui element to the drawing list for this canvas
        parameters:     dirty sprite
        return values:  -
        """
        self.sprite_list.add(spr)

    def draw(self, tgt_surface):
        """
        Update the canvas and the sprites within
        parameters:     -
        return values:  updated rects
        """
        self.sprite_list.update()
        self.sprite_list.draw(self)

        tgt_surface.blit(self, (self.x, self.y))