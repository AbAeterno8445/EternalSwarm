import pygame
import pygame.font as fnt
import MSGUI

default_font_color = (255, 255, 255)


class Label(MSGUI.Widget):
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
        super(Label, self).__init__(x, y, width, height)
        self._text = text
        self._font = font
        self._font_color = default_font_color
        self._resize_hor = False
        self._resize_ver = False
        self._padding = 0

    def set_padding(self, padding):
        """
        Set distance between text and surface borders
        parameters:     int distance in pixels
        return values:  -
        """
        self._padding = padding

    def set_auto_resize(self, res_hor=False, res_ver=False):
        """
        Set whether label surface resizes to match text width
        parameters:     boolean horizontal resizing
                        boolean vertical resizing
        return values:  -
        """
        self._resize_hor = res_hor
        self._resize_ver = res_ver

    def set_text(self, text):
        """
        Set the TextWidget's text
        parameters:     string the text to be set
        return values:  TextWidget TextWidget returned for convenience
        """
        self._text = str(text)
        self.mark_dirty()
        return self

    def get_text(self):
        """
        Return the TextWidget's text
        parameters:     -
        return values:  string the TextWidget's text
        """
        return self._text

    def set_font(self, font):
        """
        Set the TextWidget's text
        parameters:     pygame.font.Font the Font to be set
        return values:  TextWidget TextWidget returned for convenience
        """
        if isinstance(font, fnt.Font):
            self._font = font
            self.mark_dirty()
        return self

    def get_font(self):
        """
        Return the TextWidget's font
        parameters:     -
        return values:  pygame.font.Font the TextWidget's font
        """
        return self._font

    def set_font_color(self, color):
        """
        Set the displayed font's color
        parameters:     color pygame color tuple (r, g, b)
        return values:  -
        """
        self._font_color = color

    def get_font_color(self):
        """
        Return the font's color
        parameters:     -
        return values:  pygame color tuple (r, g, b)
        """
        return self._font_color

    def _get_appearance(self, *args):
        """
        Blits the text to the Label's Surface and returns the result.
        private function
        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = super(Label, self)._get_appearance(*args)
        size = self._font.size(self._text)
        if self._resize_hor or self._resize_ver:
            res_hor = surface.get_width()
            if self._resize_hor:
                res_hor = size[0]

            res_ver = surface.get_height()
            if self._resize_ver:
                res_ver = size[1]

            surface = pygame.transform.scale(surface, (res_hor + self._padding * 2,
                                                       res_ver + self._padding * 2))
        elif self._padding:
            surface = pygame.transform.scale(surface, surface.get_width() + self._padding * 2,
                                             surface.get_height() + self._padding * 2)
        center = surface.get_rect().center
        coords = (center[0] - size[0] / 2, center[1] - size[1] / 2)
        surface.blit(self._font.render(str(self._text), pygame.SRCALPHA, self._font_color), coords)
        return surface
