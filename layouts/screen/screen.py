class Screen(object):
    """
    Class for handling multiple screens. Each screen can contain multiple canvases.
    """
    def __init__(self, display):
        self.display = display
        self.canvas_list = []
        self.switch_screen = ""

    # Used to initialize screen data, called on screen switch
    # Source screen is used to get any data from the previous screen that needs to be transferred
    def init_screen(self, source_screen=None):
        pass

    def add_canvas(self, canvas):
        if type(canvas) is list:
            self.canvas_list.extend(canvas)
            for cv in canvas:
                cv.backg_widget.mark_dirty()
        else:
            self.canvas_list.append(canvas)
            canvas.backg_widget.mark_dirty()

    def remove_canvas(self, canvas):
        if canvas in self.canvas_list:
            self.canvas_list.remove(canvas)

    def get_switch_screen(self):
        old_switch = self.switch_screen
        self.switch_screen = ""
        return old_switch

    def update(self, event_list):
        upd_rects = []
        for cv in self.canvas_list:
            cv.handle_event(event_list)
            self.check_switch(cv)
            upd_rects += cv.draw(self.display)
        return upd_rects

    def check_switch(self, canvas):
        sw = canvas.get_switch()
        if sw:
            self.switch_screen = sw