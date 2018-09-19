import MSGUI


def create_canvas_materials():
    canvas_materials = MSGUI.GUICanvas(16, 16, 200, 500)
    canvas_materials.backg_widget.set_background((110, 110, 0))
    canvas_materials.backg_widget.set_border(1, (255, 0, 0))

    return canvas_materials