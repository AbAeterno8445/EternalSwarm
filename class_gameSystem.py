import pygame
from class_animSprite import AnimSprite


class GameSystem(object):
    def __init__(self, display):
        self.display = display
        self.clock = pygame.time.Clock()

        self.sprite_list = pygame.sprite.LayeredDirty()

        self.egg = AnimSprite("assets/egg.png", frames=4, anim_delay=10, img_scale=2)
        self.egg.setPosition(64, 64)
        self.sprite_list.add(self.egg)

        self.larva = AnimSprite("assets/larva.png", frames=5, anim_order=[0], img_scale=0.5)
        self.larva.setPosition(64, 256)
        self.sprite_list.add(self.larva)

    def loop(self):
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            self.display.fill((0, 0, 0))
            self.sprite_list.update()

            dirty_rects = self.sprite_list.draw(self.display)
            pygame.display.update(dirty_rects)

            self.clock.tick(60)