from .imagebox import Imagebox


class AnimSprite(Imagebox):
    def __init__(self, x, y, width, height, icon=None, frames=1, autosize=True):
        super(AnimSprite, self).__init__(x, y, width, height, icon, autosize)
        self.set_transparent(True)

        self._anim_framecount = frames
        self._anim_delay = 5
        self._anim_ticker = 0
        self._anim_order = []
        self._anim_order_pos = 0

        self._update_animation_set()

    def set_animation_order(self, order_list):
        """
        Sets the frame animation order for the sprite
        parameters:     list of ints for each frame ID in order
        return values:  -
        """
        self._anim_order = order_list

    def set_animation_delay(self, delay):
        """
        Set the delay between frames in ticks (1/60 second)
        parameters:     int delay in ticks
        return values:  -
        """
        self._anim_delay = delay

    def set_animation_data(self, frames, anim_delay=5, anim_order=None):
        """
        Set animation data for the sprite -> frame count, delay between frames and animation order
        parameters:     int frame count
                        int frame delay
                        list of ints animation order
        return values:  -
        """
        self._anim_framecount = frames
        self.set_animation_delay(anim_delay)
        if anim_order:
            self.set_animation_order(anim_order)
        else:
            self.set_animation_order([0])
        self._update_animation_set()

    def set_icon_animated(self, icon, frames, anim_delay=5, anim_order=None):
        """
        Set animation info for the sprite
        parameters:     list of ints for each frame ID in order
        return values:  -
        """
        self.set_icon(icon)
        self.set_animation_data(frames, anim_delay, anim_order)

    def _update_animation_set(self):
        """
        Updates the icon sheet for the sprite
        parameters:     -
        return values:  -
        """
        self.image_list = []
        og_texture = self.get_icon()
        frame_height = og_texture.get_height() / self._anim_framecount
        frame_width = og_texture.get_width()
        for i in range(self._anim_framecount):
            tmp_frame = og_texture.subsurface((0, i * frame_height, frame_width, frame_height))
            self.image_list.append(tmp_frame)

        if not self._anim_order:
            for i in range(self._anim_framecount):
                self._anim_order.append(i)

        self.set_icon(self.image_list[0])
        self.rect = self.image.get_rect(topleft=self.get_position())

    def update(self, *args):
        self._anim_ticker += 1
        if self._anim_ticker >= self._anim_delay:
            self.set_icon(self.image_list[self._anim_order[self._anim_order_pos]])
            self._anim_order_pos += 1
            if self._anim_order_pos >= len(self._anim_order):
                self._anim_order_pos = 0

            self._anim_ticker = 0
            self.mark_dirty()

        super(AnimSprite, self).update(*args)