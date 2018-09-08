import pygame
from class_simpleSprite import SimpleSprite
from class_animSprite import AnimSprite


class GUICanvas(pygame.Surface):
    def __init__(self, position, size):
        pygame.Surface.__init__(self, size)
        self.pos = position

        self.sprite_list = pygame.sprite.LayeredDirty()

    def set_position(self, x, y):
        self.pos = (x, y)

    def create_sprite_simple(self, image_path, position, layer=0):
        tmp_sprite = SimpleSprite(image_path)
        tmp_sprite.set_position(*position)
        self.sprite_list.add(tmp_sprite)
        self.sprite_list.change_layer(tmp_sprite, layer)
        return tmp_sprite

    def draw(self, tgt_surface):
        tgt_surface.blit(self, self.pos)