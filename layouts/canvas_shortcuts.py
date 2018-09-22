import pygame
import MSGUI


def canvas_shortcuts_create(canvas_data):
    canvas_shortcuts = MSGUI.GUICanvas(*canvas_data)
    canvas_shortcuts.set_background((0, 0, 50))
    canvas_shortcuts.backg_widget.set_border(True, (0, 0, 150))

    font = pygame.font.Font("assets/Dosis.otf", 18)
    # Terrain button
    button_terrain = MSGUI.Button(12, 10, 0, 26, font, "Terrain")
    button_terrain.set_text_resize(res_hor=True, padding=8)
    button_terrain.set_font_color((0, 200, 0))
    button_terrain.set_border(True, (50, 100, 50))
    button_terrain.set_hovered_color((100, 100, 100, 80))
    button_terrain.set_pressed_color((100, 100, 100, 150))
    canvas_shortcuts.add_element(button_terrain, widget="button_terrain")

    tmp_x = button_terrain.get_width() + 24
    # Upgrades button
    button_upgrades = MSGUI.Button(tmp_x, 10, 0, 26, font, "Upgrades")
    button_upgrades.set_text_resize(res_hor=True, padding=8)
    button_upgrades.set_font_color((0, 200, 200))
    button_upgrades.set_border(True, (50, 100, 100))
    button_upgrades.set_hovered_color((100, 100, 100, 80))
    button_upgrades.set_pressed_color((100, 100, 100, 150))
    canvas_shortcuts.add_element(button_upgrades, widget="button_upgrades")

    return canvas_shortcuts