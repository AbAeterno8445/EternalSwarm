import pygame
import MSGUI


default_hovered = (200, 200, 150, 50)
default_pressed = (200, 200, 150, 100)


class Button(MSGUI.TextWidget, MSGUI.Imagebox):

    """
    Clickable buttons with alternatively an image added
    """

    def __init__(self, x, y, width, height, font, text="", callback=None):
        """
        Initialisation of a Button
        parameters:     int x-coordinate of the Button (left)
                        int y-coordinate of the Button (top)
                        int width of the Button
                        int height of the Button
                        string text of the Button
                        pygame.font.Font font of the Button
                        function callback function to be called when Button is pressed
                return values:  -
                """
        super(Button, self).__init__(x, y, width, height, font, text)
        self._callback = callback
        self._state = 0
        self._hoveredcolor = default_hovered
        self._pressedcolor = default_pressed

    def set_hovered_color(self, color):
        """
        Set the Buttons's color overlay when hovered over
        parameters:     tuple a tuple of format pygame.Color representing the color to be set
        return values:  Widget Widget returned for convenience
        """
        self._hoveredcolor = color
        self.mark_dirty()
        return self

    def get_hovered_color(self):
        """
        Return the Buttons's color overlay when hovered over
        parameters:     -
        return values:  tuple of format pygame.Color representing the Buttons's color overlay when hovered over
        """
        return self._hoveredcolor

    def set_pressed_color(self, color):
        """
        Set the Buttons's color overlay when pressed
        parameters:     tuple a tuple of format pygame.Color representing the color to be set
        return values:  Widget Widget returned for convenience
        """
        self._pressedcolor = color
        self.mark_dirty()
        return self

    def get_pressed_color(self):
        """
        Return the Buttons's color overlay when pressed
        parameters:     -
        return values:  tuple of format pygame.Color representing the Buttons's color overlay when pressed
        """
        return self._pressedcolor

    def set_callback(self, callback):
        """
        Set the Button's callback-function
        parameters:     function function that executes on click
        return values:  Button Button returned for convenience
        """
        if callable(callback):
            self._callback = callback
        return self

    def get_callback(self):
        """
        Return the Button's callback-function
        parameters:     -
        return values:  function the Buttons's callback-function
        """
        return self._callback

    def is_hovered(self):
        """
        Return if the Button is hovered over
        parameters:     -
        return values:  boolean is the Button hovered over
        """
        return self._state == 1

    def is_pressed(self):
        """
        Return if the Button is pressed
        parameters:     -
        return values:  boolean is the Button pressed
        """
        return self._state >= 2

    def _change_state(self, state):
        """
        Changes the state of the button (0 normal, 1 hovered, 2 pressed)
        parameters:     int new button state
        return values:  -
        """
        self._state = state
        self.mark_dirty()

    def update(self, *args):
        """
        Handles the clicking of the Button and calls the function given in the constructor.
        parameters: tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values: -
        """
        if len(args) > 0 and self.is_active():
            event = args[0]
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if event.button == 1:
                        if self._state >= 2:
                            self._change_state(1)
                        try:
                            self._callback()
                        except Exception as e:
                            print(e)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if event.button == 1:
                        self._change_state(2)
                    else:
                        self._change_state(1)
            elif event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if event.buttons[0]:
                        self._change_state(2)
                    else:
                        self._change_state(1)
                elif self._state:
                    if self._state >= 2:
                        self._change_state(1)
                    else:
                        self._change_state(0)

        super(Button, self).update(*args)

    def _get_appearance(self, *args):
        """
        Blits the text to the Button's Surface and returns the result.
        private function
        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = super(Button, self)._get_appearance(*args)
        center = surface.get_rect().center
        size = self._font.size(self._text)
        coords = (center[0] - size[0] / 2, center[1] - size[1] / 2)
        surface.blit(self._font.render(str(self._text), pygame.SRCALPHA, self._font_color), coords)
        if self._state:
            overlay = pygame.Surface(surface.get_size()).convert()
            if self._state == 2:
                overlay.fill(self._pressedcolor)
            else:
                overlay.fill(self._hoveredcolor)
            overlay.set_alpha(120)
            surface.blit(overlay, (0, 0))
        return surface