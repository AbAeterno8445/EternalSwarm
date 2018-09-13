import pygame.font as fnt
import MSGUI

default_font_color = (255, 255, 255)


class TextWidget(MSGUI.Widget):
    """
    Underlying class for Widgets using text/strings;
    """

    def __init__(self, x, y, width, height, font, text=""):
        """
        Initialisation of a TextWidget
        parameters:     int x-coordinate of the TextWidget (left)
                        int y-coordinate of the TextWidget (top)
                        int width of the TextWidget
                        int height of the TextWidget
                        string text of the TextWidget
                        pygame.font.Font font of the TextWidget
        return values:  -
        """
        super(TextWidget, self).__init__(x, y, width, height)
        self._text = text
        self._font = font
        self._font_color = default_font_color

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