import pygame


class SimpleSprite(pygame.sprite.DirtySprite):
    def __init__(self, image_path):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect = self.image.get_rect(topleft=(x, y))