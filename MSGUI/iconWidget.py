import pygame
import math
from .widget import Widget


class IconWidget(Widget):
    """
    Underlying class for Widgets using icons/surfaces/images;
    """

    def __init__(self, x, y, width, height, icon=None, autosize=False):
        """
        Initialisation of a IconWidget
        parameters:     int x-coordinate of the IconWidget (left)
                        int y-coordinate of the IconWidget (top)
                        int width of the IconWidget
                        int height of the IconWidget
                        pygame.Surface icon/surface of the IconWidget
        return values:  -
        """
        super(IconWidget, self).__init__(x, y, width, height)
        self._autosize = autosize
        if icon is None:
            icon = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        elif type(icon) is str:
            icon = pygame.image.load(icon)
        self.set_icon(icon)

    def set_icon_autosize(self, autosize):
        """
        Set whether IconWidget's surface automatically resizes when setting icon
        parameters:     boolean resizes
        return values:  -
        """
        self._autosize = autosize

    def _autoresize(self):
        self.set_bounds(self._icon.get_rect(topleft=self._bounds.topleft))

    def set_icon(self, icon):
        """
        Set the IconWidget's icon/surface
        parameters:     pygame.Surface icon/surface to be set
        return values:  IconWidget IconWidget returned for convenience
        """
        if isinstance(icon, pygame.Surface):
            self._icon = icon.convert_alpha(super(IconWidget, self)._get_appearance())
            self.mark_dirty()
        elif type(icon) is str:
            self._icon = pygame.image.load(icon).convert_alpha(super(IconWidget, self)._get_appearance())
            self.mark_dirty()

        if self._autosize:
            self._autoresize()
        return self

    def get_icon(self):
        """
        Return the IconWidget's icon/surface
        parameters:     -
        return values:  pygame.Surface icon/surface of the IconWidget
        """
        return self._icon