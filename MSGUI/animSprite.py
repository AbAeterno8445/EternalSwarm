import pygame
import math


class AnimSprite(pygame.sprite.DirtySprite):
    def __init__(self, image_path, frames, anim_delay=5, img_scale=1, anim_order=None):
        pygame.sprite.DirtySprite.__init__(self)

        self.x = 0
        self.y = 0

        self.anim_framecount = frames
        self.anim_speed = anim_delay
        self.anim_ticker = 0
        self.anim_order = []
        self.anim_order_pos = 0
        if not anim_order:
            for i in range(self.anim_framecount):
                self.anim_order.append(i)
        else:
            self.anim_order = anim_order

        self.image_list = []
        og_texture = pygame.image.load(image_path)
        frame_height = og_texture.get_height() / self.anim_framecount
        frame_width = og_texture.get_width()
        for i in range(self.anim_framecount):
            tmp_frame = og_texture.subsurface((0, i * frame_height, frame_width, frame_height))
            if not img_scale == 1:
                tmp_frame = pygame.transform.scale(tmp_frame, (math.floor(frame_width * img_scale),
                                                               math.floor(frame_height * img_scale)))
            self.image_list.append(tmp_frame)

        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.dirty = 1

    def setPosition(self, x, y):
        self.x, self.y = x, y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dirty = 1

    def update(self):
        self.anim_ticker += 1
        if self.anim_ticker >= self.anim_speed:
            self.image = self.image_list[self.anim_order[self.anim_order_pos]]
            self.anim_order_pos += 1
            if self.anim_order_pos >= len(self.anim_order):
                self.anim_order_pos = 0

            self.anim_ticker = 0
            self.dirty = 1