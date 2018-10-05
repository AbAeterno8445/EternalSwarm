import MGUI


class CanvasSwitcher(MGUI.GUICanvas):
    """
    Subclasses GUICanvas, provides functionality for canvas switching in main.py
    """
    def __init__(self, x, y, width, height, bgcolor=None):
        if bgcolor:
            super().__init__(x, y, width, height, bgcolor)
        else:
            super().__init__(x, y, width, height)

        self.switch_cvname = ""

    def switch_canvas(self, newcanvas):
        self.switch_cvname = newcanvas

    def get_switch_canvas(self):
        old_cvname = self.switch_cvname
        self.switch_cvname = ""
        return old_cvname