import pygame
from .image_widget import ImageWidget


class AnimSprite(ImageWidget):
    def __init__(self, x, y, width, height, icon=None, frames=1, autosize=True):
        super().__init__(x, y, width, height, icon, autosize, smooth=True)

        self.image_list = []
        self.image_list_modified = []

        self._anim_framecount = frames
        self._anim_delay = 5
        self._anim_ticker = 0
        self._anim_order = []
        self._anim_order_pos = 0

        self._update_animation_set(self._icon)
        self.set_icon_autoscale(True)

    def _update_animation_set(self, new_icon=None):
        """
        Updates the icon sheet for the sprite
        parameters:     pygame.Surface new icon sheet, leave as none to update current loaded sheet
        return values:  -
        """
        self.image_list_modified = []
        if new_icon:
            if type(new_icon) is str:
                new_icon = pygame.image.load(new_icon)
            og_texture = new_icon
            self._anim_order = []
            self.image_list = []
            frame_height = og_texture.get_height() / self._anim_framecount
            frame_width = og_texture.get_width()
            for i in range(self._anim_framecount):
                tmp_frame = og_texture.subsurface((0, i * frame_height, frame_width, frame_height))
                self.set_icon(tmp_frame)
                self.image_list.append(self._icon)
        else:
            for i in range(len(self.image_list)):
                self.set_icon(self.image_list[i])
                self.image_list_modified.append(self._icon)

        if not self._anim_order:
            new_anim_order = []
            for i in range(self._anim_framecount):
                new_anim_order.append(i)
            self.set_animation_order(new_anim_order)

    def set_icon_autosize(self, autosize):
        super().set_icon_autosize(autosize)
        self._update_animation_set()

    def set_icon_autoscale(self, autoscale):
        super().set_icon_autoscale(autoscale)
        self._update_animation_set()

    def set_bounds_size(self, width, height):
        super().set_bounds_size(width, height)
        self._update_animation_set()

    def set_animation_order(self, order_list):
        """
        Sets the frame animation order for the sprite
        parameters:     list of ints for each frame ID in order
        return values:  -
        """
        self._anim_order = order_list
        if self._anim_order_pos > len(self._anim_order):
            self._anim_order_pos = 0

    def set_animation_delay(self, delay):
        """
        Set the delay between frames in ticks (1/60 second)
        parameters:     int delay in ticks
        return values:  -
        """
        self._anim_delay = delay

    def set_icon_animated(self, icon, frames, anim_delay=5, anim_order=None):
        """
        Set animation info and icon for the sprite
        parameters:     list of ints for each frame ID in order
        return values:  -
        """
        self._anim_framecount = frames
        self.set_animation_delay(anim_delay)
        if anim_order:
            self.set_animation_order(anim_order)
        self._update_animation_set(icon)

    def update(self, *args):
        self._anim_ticker += 1
        if self._anim_ticker >= self._anim_delay:
            if not self.image_list_modified:
                self._icon = self.image_list[self._anim_order[self._anim_order_pos]]
            else:
                self._icon = self.image_list_modified[self._anim_order[self._anim_order_pos]]
            self._anim_order_pos += 1
            if self._anim_order_pos >= len(self._anim_order):
                self._anim_order_pos = 0

            self._anim_ticker = 0
            self.mark_dirty()

        super().update(*args)