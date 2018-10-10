import pygame
from .label import Label

default_cursor_color = (255, 255, 255)
valid_characters = " `1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?"


class InputBox(Label):
    def __init__(self, x, y, width, height, font, text=""):
        super().__init__(x, y, width, height, font, text)

        self.charlimit = 100
        self._held_key = None
        self._held_key_uc = None
        self._held_key_time = 0
        self._hold_delay = 35

        self._cursor_pos = len(text)
        self._cursor_color = default_cursor_color
        self._cursor_ticker = 0
        self._cursor_visible = True

        self._old_color = None
        self._selected_color = None
        self._old_color_bg = None
        self._selected_color_bg = None

    def set_character_limit(self, limit):
        self.charlimit = limit

    def set_cursor_color(self, color):
        self._cursor_color = color

    def set_selected_bordercolor(self, color):
        self._selected_color = color

    def set_selected_backgcolor(self, color):
        self._selected_color_bg = color

    def set_focused(self, focused):
        super().set_focused(focused)
        if focused:
            self._cursor_pos = len(self._text)
            self._cursor_ticker = 0
            if self._selected_color:
                self._old_color = self.get_border_color()
                self.set_border(self.has_border(), self._selected_color)
            if self._selected_color_bg:
                self._old_color_bg = self.get_background()
                self.set_background(self._selected_color_bg)
        else:
            if self._selected_color:
                self.set_border(self.has_border(), self._old_color)
            if self._selected_color_bg:
                self.set_background(self._old_color_bg)

    def press_key(self, key, unicode):
        if key == pygame.K_ESCAPE or key == pygame.K_RETURN:
            self.set_focused(False)
        else:
            # Reset cursor on keypress for visibility
            self._cursor_ticker = 0
            self.mark_dirty()

            if key == pygame.K_BACKSPACE:  # Backspace
                if len(self._text) > 0:
                    text_mod = self._text[:max(0, self._cursor_pos - 1)] + self._text[self._cursor_pos:]
                    self.set_text(text_mod)
                    self._cursor_pos = max(0, self._cursor_pos - 1)

            elif key == pygame.K_DELETE:  # Delete button
                if len(self._text) > 0:
                    text_mod = self._text[:self._cursor_pos] + self._text[self._cursor_pos + 1:]
                    self.set_text(text_mod)

            elif key == pygame.K_LEFT:  # Move cursor left
                self._cursor_pos = max(0, self._cursor_pos - 1)

            elif key == pygame.K_RIGHT:  # Move cursor right
                self._cursor_pos = min(len(self._text), self._cursor_pos + 1)

            elif key == pygame.K_HOME:  # Move cursor to the start
                self._cursor_pos = 0

            elif key == pygame.K_END:  # Move cursor to the end
                self._cursor_pos = len(self._text)

            elif unicode in valid_characters and len(self._text) < self.charlimit:  # Add character to text
                text_mod = self._text[:self._cursor_pos] + unicode + self._text[self._cursor_pos:]
                self.set_text(text_mod)
                self._cursor_pos += len(unicode)

    def handle_event(self, event):
        super().handle_event(event)

        if self.is_focused():
            if event.type == pygame.KEYDOWN:
                self._held_key = event.key
                self._held_key_uc = event.unicode
                self._held_key_time = 0
                self.press_key(event.key, event.unicode)
            elif event.type == pygame.KEYUP:
                if event.key == self._held_key:
                    self._held_key = None
        else:
            self._cursor_visible = False
            self._cursor_ticker = 0

    def update(self, *args):
        # Cursor
        if self.is_focused():
            self._cursor_ticker = (self._cursor_ticker + 1) % 60
            if self._cursor_ticker >= 30 and self._cursor_visible:
                self._cursor_visible = False
                self.mark_dirty()
            elif self._cursor_ticker < 30 and not self._cursor_visible:
                self._cursor_visible = True
                self.mark_dirty()

        # Handle held keys
        if self._held_key:
            if self._held_key_time < self._hold_delay:
                self._held_key_time += 1
            else:
                self._held_key_time -= 1  # Slow repetition down (too quick otherwise)
                self.press_key(self._held_key, self._held_key_uc)

        super().update(*args)

    def _get_appearance(self, *args):
        surface = super()._get_appearance(*args)
        if self._cursor_visible:
            cursor_x = self.get_width() / 2 - self._font.size(self._text)[0] / 2 + self._font.size(self._text[:self._cursor_pos])[0]
            pygame.draw.line(surface, self._cursor_color, (cursor_x, 4), (cursor_x, self.get_height() - 5))
        return surface