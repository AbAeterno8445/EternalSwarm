import pygame
from .widget import Widget


class ImageWidget(Widget):
    """
    Underlying class for Widgets using icons/surfaces/images;
    """

    def __init__(self, x, y, width, height, icon=None, autosize=False, smooth=False):
        """
        Initialisation of a ImageWidget
        parameters:     int x-coordinate of the ImageWidget (left)
                        int y-coordinate of the ImageWidget (top)
                        int width of the ImageWidget
                        int height of the ImageWidget
                        pygame.Surface icon/surface of the ImageWidget
        return values:  -
        """
        super().__init__(x, y, width, height)
        self.set_transparent(True)
        self._alpha = 255
        self._smooth = smooth
        self._autosize = autosize
        self._autoscale = False
        self._rotation = 0
        self._flip_hor = False
        self._flip_ver = False
        if icon is None:
            icon = super()._get_appearance()
        elif type(icon) is str:
            icon = pygame.image.load(icon)
        self.set_icon(icon)

    def set_smooth(self, smooth):
        """
        Set the smoothing of the surface/image when scaling to the bounds of the Imagebox
        parameters:     boolean if the surface/image should be scaled smoothly
        return values:  Imagebox Imagebox returned for convenience
        """
        self._smooth = bool(smooth)
        self.mark_dirty()
        return self

    def set_alpha(self, alpha):
        """
        Set the Widget's alpha value
        parameters:     int alpha value 0-255
        return values:  -
        """
        self._alpha = max(0, min(255, alpha))
        self.mark_dirty()

    def get_alpha(self):
        """
        Return the Widget's alpha value
        parameters:     -
        return values:  int widget's alpha value
        """
        return self._alpha

    def set_icon_autoscale(self, autoscale):
        """
        Set whether the icon resizes automatically to fit the widget's bounds
        parameters:     boolean resizes
        return values:  -
        """
        self._autoscale = autoscale
        if self._icon:
            self.set_icon(self._icon)

    def set_icon_autosize(self, autosize):
        """
        Set whether ImageWidget's surface automatically resizes when setting icon
        parameters:     boolean resizes
        return values:  -
        """
        self._autosize = autosize
        if self._icon:
            self.set_icon(self._icon)

    def set_rotation(self, angle):
        self._rotation = angle
        self.mark_dirty()

    def set_flip(self, flip_hor=False, flip_ver=False):
        self._flip_hor = flip_hor
        self._flip_ver = flip_ver
        self.mark_dirty()

    def _apply_autosize(self):
        self.set_bounds(self._icon.get_rect(topleft=self._bounds.topleft))

    def _apply_autoscale(self):
        rect_fit = self._icon.get_rect().fit(self._bounds)
        if self._smooth:
            self._icon = pygame.transform.smoothscale(self._icon, rect_fit.size)
        else:
            self._icon = pygame.transform.scale(self._icon, rect_fit.size)

    def _apply_rotation(self):
        self._icon = pygame.transform.rotate(self._icon, self._rotation)

    def _apply_flip(self):
        self._icon = pygame.transform.flip(self._icon, self._flip_hor, self._flip_ver)

    def set_icon(self, icon):
        """
        Set the ImageWidget's icon/surface
        parameters:     pygame.Surface icon/surface to be set
        return values:  ImageWidget ImageWidget returned for convenience
        """
        if isinstance(icon, pygame.Surface):
            self._icon = icon.convert_alpha(super()._get_appearance())
        elif type(icon) is str:
            self._icon = pygame.image.load(icon).convert_alpha(super()._get_appearance())

        if self._autosize:
            self._apply_autosize()
        elif self._autoscale:
            self._apply_autoscale()

        if self._rotation:
            self._apply_rotation()
        if self._flip_hor or self._flip_ver:
            self._apply_flip()

        self.mark_dirty()
        return self

    def get_icon(self):
        """
        Return the ImageWidget's icon/surface
        parameters:     -
        return values:  pygame.Surface icon/surface of the ImageWidget
        """
        return self._icon

    def _get_appearance(self, *args):
        """
        Blits the Imagebox's Surface and returns the result.
        private function
        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = super()._get_appearance(*args)

        centerpos_x = abs(self._bounds.width / 2 - self._icon.get_width() / 2)
        centerpos_y = abs(self._bounds.height / 2 - self._icon.get_height() / 2)

        for tries in range(2):
            try:
                if self._smooth:
                    surface.blit(pygame.transform.smoothscale(self._icon, self._icon.get_size()), (centerpos_x, centerpos_y))
                else:
                    surface.blit(pygame.transform.scale(self._icon, self._icon.get_size()), (centerpos_x, centerpos_y))

                break
            except:
                self._icon = self._icon.convert_alpha(surface)
        else:
            self._icon = surface

        if not self._alpha == 255:
            surface.set_alpha(self._alpha)
        return surface