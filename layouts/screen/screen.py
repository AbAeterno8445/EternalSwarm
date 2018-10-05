class Screen(object):
    """
    Class for handling multiple screens. Each screen can contain multiple canvases.
    """
    def __init__(self):
        self.canvas_dict = {}

    def handle_event(self, event_list):
        for cv in self.canvas_dict:
            self.canvas_dict[cv].handle_event(event_list)