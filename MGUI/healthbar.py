import pygame
import math
from .widget import Widget


default_hbar_color = (0, 200, 0)


class Healthbar(Widget):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self._mode = 0  # 0 uses percentage, 1 calculates between min and max val

        self._perc = 1
        self._color = default_hbar_color
        self._val = 0
        self._max_val = 0

    # Sets draw mode to percentage based
    def set_percentage(self, perc):
        if not perc == self._perc:
            self._perc = perc
            self._mode = 0
            self.mark_dirty()

    # Sets draw mode to value based
    def set_value(self, minval):
        self._val = minval
        self._mode = 1
        self.mark_dirty()

    # Sets draw mode to value based
    def set_maximum_value(self, maxval):
        if not self._max_val == maxval:
            self._max_val = maxval
            self._mode = 1
            self.mark_dirty()

    def set_color(self, color):
        self._color = color
        self.mark_dirty()

    def _get_appearance(self, *args):
        surface = super()._get_appearance(*args)
        if self._mode == 1:
            mult = self._val / self._max_val
        else:
            mult = self._perc
        mult = min(1, max(0, mult))
        rect_len = math.floor(surface.get_width() * mult)
        pygame.draw.rect(surface, self._color, (0, 0, rect_len, surface.get_height()))
        return surface