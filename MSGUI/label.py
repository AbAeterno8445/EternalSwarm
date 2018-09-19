import pygame
from .textWidget import TextWidget


class Label(TextWidget):
    def __init__(self, x, y, width, height, font, text=""):
        """
        Initialisation of a TextWidget
        parameters:     int x-coordinate of the TextWidget (left)
                        int y-coordinate of the TextWidget (top)
                        int width of the TextWidget
                        int height of the TextWidget
                        pygame.font.Font font of the TextWidget
                        string text of the TextWidget
        return values:  -
        """
        super().__init__(x, y, width, height, font, text)
        self._text = text
        self._font = font

        self._resize_hor = False
        self._resize_ver = False
        self._padding = 0

    def set_text_resize(self, res_hor=False, res_ver=False, padding=0):
        """
        Set whether label surface resizes to match text width
        parameters:     boolean horizontal resizing
                        boolean vertical resizing
                        int padding in pixels
        return values:  -
        """
        self._resize_hor = res_hor
        self._resize_ver = res_ver
        self._padding = padding

    def _get_appearance(self, *args):
        """
        Blits the text to the Label's Surface and returns the result.
        private function
        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        if self._text:
            size = self._font.size(self._text)
            if self._resize_hor or self._resize_ver:
                res_hor = self._bounds.width
                if self._resize_hor:
                    res_hor = size[0] + self._padding * 2

                res_ver = self._bounds.height
                if self._resize_ver:
                    res_ver = size[1] + self._padding * 2

                self.set_bounds_size(res_hor, res_ver)

            surface = super()._get_appearance(*args)

            center = surface.get_rect().center
            coords = (center[0] - size[0] / 2, center[1] - size[1] / 2)
            surface.blit(self._font.render(str(self._text), pygame.SRCALPHA, self._font_color, self._background), coords)
            return surface
        return super()._get_appearance(*args)