import MSGUI
from game_map import GameMap


class CanvasGame(MSGUI.GUICanvas):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.backg_widget.set_border(True, (200, 200, 200))