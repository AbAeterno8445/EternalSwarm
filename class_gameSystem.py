import pygame
from class_guiCanvas import GUICanvas
from class_animSprite import AnimSprite
from class_simpleSprite import SimpleSprite


class GameSystem(object):
    def __init__(self, display):
        self.display = display
        self.clock = pygame.time.Clock()

        self.sprite_list = pygame.sprite.LayeredDirty()

        self.background = SimpleSprite("assets/bg.png")
        self.sprite_list.add(self.background)
        self.sprite_list.change_layer(self.background, 0)

        self.egg = AnimSprite("assets/egg.png", frames=4, anim_delay=10, img_scale=2)
        self.egg.setPosition(64, 64)
        self.sprite_list.add(self.egg)
        self.sprite_list.change_layer(self.egg, 1)

        self.larva = AnimSprite("assets/larva.png", frames=5, anim_order=[0])
        self.larva.setPosition(64, 256)
        self.sprite_list.add(self.larva)
        self.sprite_list.change_layer(self.larva, 1)

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