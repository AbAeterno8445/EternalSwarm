import pygame
import MSGUI


def canvas_materials_create(canvas_data, player_data):
    canvas_materials = MSGUI.GUICanvas(*canvas_data)
    canvas_materials.backg_widget.set_background((40, 0, 40))
    canvas_materials.backg_widget.set_border(True, (110, 40, 110))

    font_18 = pygame.font.Font("assets/Dosis.otf", 18)
    font_12 = pygame.font.Font("assets/Dosis.otf", 12)
    # Player name
    plname_label = MSGUI.Label(8, 8, canvas_materials.get_width() - 16, 24, font_18, player_data.name)
    plname_label.set_background((15, 0, 15))
    plname_label.set_border(True, (110, 40, 110))
    plname_label.set_font_color((255, 200, 255))
    canvas_materials.add_element(plname_label)

    # Crystal image
    crystal_button = MSGUI.ImageWidget(8, 40, 64, 64, "assets/materials/carbcrystal.png")
    crystal_button.set_icon_autoscale(True)
    canvas_materials.add_element(crystal_button, widget="crystal_button")

    tmp_width = canvas_materials.get_width() - 68
    # Crystal amount number label
    crystal_amt_text = MSGUI.Label(68, 40, tmp_width, 22, font_18, "0")
    crystal_amt_text.set_transparent(True)
    canvas_materials.add_element(crystal_amt_text, widget="crystal_amt_text")

    # "Carbonic crystals" label
    crystal_text = MSGUI.Label(68, 62, tmp_width, 22, font_18, "Carbonic crystals")
    crystal_text.set_transparent(True)
    canvas_materials.add_element(crystal_text, widget="crystal_text")

    # Crystals per second label
    ccps_text = MSGUI.Label(68, 84, tmp_width, 22, font_12, "0 CCps")
    ccps_text.set_transparent(True)
    canvas_materials.add_element(ccps_text, widget="ccps_text")

    return canvas_materials