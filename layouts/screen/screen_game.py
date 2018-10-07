from .screen import Screen
import layouts


class ScreenGame(Screen):
    def __init__(self, display, player_data):
        super().__init__(display)
        self.player_data = player_data

        self.cv_game = layouts.CanvasGame(0, 0, *display.get_size(), player_data)
        self.add_canvas(self.cv_game)

    def init_screen(self, source_screen=None):
        if source_screen:
            # Initialize game from level info screen
            if isinstance(source_screen, layouts.ScreenLevelInfo):
                self.cv_game.init_data(source_screen.selected_tile)