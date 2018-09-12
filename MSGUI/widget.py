import pygame


default_background = (0, 0, 0)
default_hover = (130, 130, 130)
default_border = (255, 255, 255)
disabled_overlay = (150, 150, 150, 150)


class Widget(pygame.sprite.DirtySprite):

    """
    Underlying class for interactive GUI-objects with PyGame;
    extends pygame.sprite.DirtySprite
    intended for use together with pygame.sprite.LayeredDirty
    """

    def __init__(self, x, y, width, height):
        """
        Initialisation of a Widget
        parameters:     int x-coordinate of the Widget (left)
                        int y-coordinate of the Widget (top)
                        int width of the Widget
                        int height of the Widget
        return values:  -
        """
        super(Widget, self).__init__()
        self.x, self.y = x, y
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self._bounds = self.image.get_rect().move(x, y)
        self.rect = self._bounds.copy()
        self._border = False
        self._border_color = default_border
        self._hover = False     # Changes color when hovered
        self._hovered = False   # Currently hovered
        self._hover_color = default_hover
        self._focus = False
        self._active = True
        self._background = default_background
        self._default_background = self._background

    def mark_dirty(self):
        """
        Mark the Widget as dirty and therefore to be redrawn in the next cycle
        parameters:     -
        return values:  -
        """
        if not self.dirty >= 2:
            self.dirty = 1

    def mark_dirty_forever(self):
        """
        Mark the Widget as constantly dirty and therefore to be redrawn periodically
        parameters:     -
        return values:  -
        """
        self.dirty = 2

    def mark_clean(self):
        """
        Mark the Widget as clean and therefore not to be redrawn in the next cycle
        parameters:     -
        return values:  -
        """
        self.dirty = 0

    def is_dirty(self):
        """
        Return if the Widget is dirty and will be redrawn in the next cycle
        parameters:     -
        return values:  boolean is the Widget dirty
        """
        return self.dirty >= 1

    def set_visible(self, visible):
        """
        Set the Widget as visible
        parameters:     boolean if the Widget should be visible
        return values:  Widget Widget returned for convenience
        """
        if self.visible != bool(visible):
            self.visible = bool(visible)
            self.set_active(bool(visible))
        return self

    def is_visible(self):
        """
        Return if the Widget is visible
        parameters:     -
        return values:  boolean is the Widget visible
        """
        return self.visible

    def set_focused(self, focused):
        """
        Set the Widget as focused
        parameters:     boolean if the Widget should be focused
        return values:  Widget Widget returned for convenience
        """
        if self._focus != bool(focused):
            self._focus = bool(focused)
            self.mark_dirty()
        return self

    def is_focused(self):
        """
        Return if the Widget is focused
        parameters:     -
        return values:  boolean is the Widget focused
        """
        return self._focus

    def set_active(self, active):
        """
        Set the Widget as active and therefore as interactive
        parameters:     boolean if the Widget should be active
        return values:  Widget Widget returned for convenience
        """
        if self._active != bool(active):
            self._active = bool(active)
            self.mark_dirty()
        return self

    def is_active(self):
        """
        Return if the Widget is active
        parameters:     -
        return values:  boolean is the Widget active
        """
        return self._active

    def set_bounds(self, rect):
        """
        Set the Widget's bounds
        parameters:     pygame.Rect the Rect to be set
        return values:  Widget Widget returned for convenience
        """
        self._bounds = rect
        self.mark_dirty()
        return self

    def get_bounds(self):
        """
        Return the Widget's bounds
        parameters:     -
        return values:  pygame.Rect the bounds of the Widget
        """
        return self._bounds

    def set_border(self, border, border_color=default_border):
        """
        Return the Widget's bounds
        parameters:     boolean has border
                        pygame.Color border color
        return values:  -
        """
        self._border = border
        self._border_color = border_color

    def get_border_color(self):
        """
        Returns the widget's border color
        parameters:     -
        return values:  pygame.Color the border color
        """
        return self._border_color

    def has_border(self):
        """
        Returns whether the widget has a border
        parameters:     -
        return values:  boolean has border
        """
        return self._border

    def set_background(self, color, transparent=False):
        """
        Set the Widget's background-color
        parameters:     tuple a tuple of format pygame.Color representing the color to be set
        return values:  Widget Widget returned for convenience
        """
        self._background = color
        self._default_background = color
        if transparent:
            self.image.set_colorkey(color)
        self.mark_dirty()
        return self

    def get_background(self):
        """
        Return the Widget's background-color
        parameters:     -
        return values:  tuple of format pygame.Color representing the Widget's background-color
        """
        return self._background

    def set_hovered(self, hover, hover_color=None):
        """
        Set whether the widget's background changes when hovered by the mouse, sets the color as well
        parameters:     boolean can be hovered
                        pygame.Color hover background color
        return values:  -
        """
        self._hover = hover
        if not hover_color:
            hover_r, hover_g, hover_b = self._background
            self._hover_color = (min(255, hover_r + 50),
                                 min(255, hover_g + 50),
                                 min(255, hover_b + 50))
        else:
            self._hover_color = hover_color

    def is_hoverable(self):
        """
        Return whether the widget changes background color when hovered by mouse
        parameters:     -
        return values:  boolean hoverable
        """
        return self._hover

    def update(self, *args):
        """
        Perform any updates on the Widget if needed;
        basic implementation of focus, hover, active-state and border-rendering;
        used for interaction in more advanced, derivated Widget-classes
        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  -
        """
        if self.is_active() and len(args) > 0:
            event = args[0]
            # Hover background color change
            if self._hover:
                if event.type == pygame.MOUSEMOTION:
                    if self._bounds.collidepoint(event.pos) :
                        self._hovered = True
                        self._background = self._hover_color
                        self.mark_dirty()
                    else:
                        self._hovered = False
                        self._background = self._default_background
                        self.mark_dirty()
            elif not self._background == self._default_background:
                self._background = self._default_background
                self.mark_dirty()

            # Set focus on click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 2, 3):
                self.set_focused(self.rect.collidepoint(event.pos))

        # Update if dirty
        if self.is_dirty():
            self.image = self._get_appearance(*args)
            # Change bounds size if image appearance is bigger/smaller
            if not self.image.get_rect().size == self._bounds.size:
                self._bounds = self.image.get_rect(topleft=self._bounds.topleft).copy()

            self.rect = self._bounds.copy()

            if self._border:
                pygame.draw.rect(self.image, self._border_color, (0, 0, self.rect.width, self.rect.height), 1)

            if not self.is_active():
                inactive = self.image.copy()
                inactive.fill(disabled_overlay)
                self.image.blit(inactive, (0, 0))

    def _get_appearance(self, *args):
        """
        Return the underlying Widget's appearance;
        basic implementation of background-coloring
        private function
        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = pygame.Surface(self._bounds.size, pygame.SRCALPHA)
        surface.fill(self._background)
        return surface