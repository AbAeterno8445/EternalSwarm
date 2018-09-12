import pygame
import math


class SimpleSprite(pygame.sprite.DirtySprite):
    def __init__(self, image_path, img_scale=1):
        pygame.sprite.DirtySprite.__init__(self)

        self.x = 0
        self.y = 0
        self.image = pygame.image.load(image_path)
        if not img_scale == 1:
            self.image = pygame.transform.scale(self.image, (math.floor(self.image.get_width() * img_scale),
                                                             math.floor(self.image.get_height() * img_scale)))
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.x, self.y = x, y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dirty = 1