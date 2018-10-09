from .screen import Screen
import layouts


class ScreenGame(Screen):
    def __init__(self, display, player_data):
        super().__init__(display)
        self.player_data = player_data
        self.victory = False
        self.level_tile = None

        self.cv_game = layouts.CanvasGame(0, 0, *display.get_size(), player_data)
        self.add_canvas(self.cv_game)

    def init_screen(self, source_screen=None):
        super().init_screen(source_screen)
        if source_screen:
            # Initialize game from level info screen
            if isinstance(source_screen, layouts.ScreenLevelInfo):
                self.level_tile = source_screen.selected_tile
                self.cv_game.init_data(self.level_tile)

    def update(self, event_list):
        upd_rects = super().update(event_list)
        self.victory = self.cv_game.victory
        return upd_rects