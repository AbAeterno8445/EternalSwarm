from .screen import Screen
import layouts


class ScreenLevelInfo(Screen):
    def __init__(self, display):
        super().__init__(display)
        self.selected_tile = None

        self.cv_levelinfo = layouts.CanvasLevelInfo(0, 0, *display.get_size())
        self.add_canvas(self.cv_levelinfo)

    def init_screen(self, source_screen=None):
        if source_screen:
            # Init screen from main screen
            if isinstance(source_screen, layouts.ScreenMain):
                self.selected_tile = source_screen.terrain_selected
                # If somehow there's no source tile to get level info from, return to main
                if not self.selected_tile:
                    self.switch_screen = "main"
                else:
                    self.cv_levelinfo.init_data(self.selected_tile)