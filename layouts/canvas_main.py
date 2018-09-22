import MSGUI


def canvas_main_create(canvas_data=None):
    canvas_main = MSGUI.GUICanvas(*canvas_data)
    canvas_main.backg_widget.set_background((0, 110, 110))
    canvas_main.backg_widget.set_border(True, (0, 150, 150))

    return canvas_main