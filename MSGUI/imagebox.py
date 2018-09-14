import pygame
from .iconWidget import IconWidget


class Imagebox(IconWidget):
    """
    Imagebox for displaying surfaces/images
    """

    def __init__(self, x, y, width, height, icon=None, autosize=False, smooth=False):
        """
        Initialisation of a Imagebox
        parameters:     int x-coordinate of the Imagebox (left)
                        int y-coordinate of the Imagebox (top)
                        int width of the Imagebox
                        int height of the Imagebox
                        pygame.Surface surface/image of the Imagebox
                        boolean if the surface/image should be scaled smoothly
                return values:  -
                """
        super(Imagebox, self).__init__(x, y, width, height, icon, autosize)
        self._smooth = smooth

    def set_smooth(self, smooth):
        """
        Set the smoothing of the surface/image when scaling to the bounds of the Imagebox
        parameters:     boolean if the surface/image should be scaled smoothly
        return values:  Imagebox Imagebox returned for convenience
        """
        self._smooth = bool(smooth)
        self.mark_dirty()
        return self

    def is_smooth(self):
        """
        Return if the surface/image is being scaled smoothly
        parameters:     -
        return values:  boolean is the surface/image being scaled smoothly
        """
        return self._smooth

    def _get_appearance(self, *args):
        """
        Blits the Imagebox's Surface and returns the result.
        private function
        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = super(Imagebox, self)._get_appearance(*args)

        for tries in range(2):
            try:
                if self._smooth:
                    surface.blit(pygame.transform.smoothscale(self._icon, self._bounds.size), (0, 0))
                else:
                    surface.blit(pygame.transform.scale(self._icon, self._bounds.size), (0, 0))

                break
            except:
                self._icon = self._icon.convert_alpha(surface)
        else:
            self._icon = surface

        return surface