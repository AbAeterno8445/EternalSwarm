import MGUI


class CanvasSwitcher(MGUI.GUICanvas):
    """
    Subclasses GUICanvas, provides functionality for canvas switching
    """
    def __init__(self, x, y, width, height, bgcolor=None):
        if bgcolor:
            super().__init__(x, y, width, height, bgcolor)
        else:
            super().__init__(x, y, width, height)

        self.switch_tgtname = ""

    def switch_target(self, newtarget):
        self.switch_tgtname = newtarget

    # Runs when a canvas gets switched to
    def on_switch(self):
        pass

    def get_switch(self):
        old_cvname = self.switch_tgtname
        self.switch_tgtname = ""
        return old_cvname