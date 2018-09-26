import pygame
import MSGUI


class TerrainLevelinfo(MSGUI.WidgetCollection):
    def __init__(self, x, y, width, height):
        super().__init__()

        backg_widget = MSGUI.Widget(x, y, width, height)
        backg_widget.set_background((20, 20, 20, 150))
        backg_widget.set_border(True)
        self.add_widget(backg_widget, "background")

        font = pygame.font.Font("assets/Dosis.otf", 18)
        # Region name
        region_label = MSGUI.Label(8, 8, 0, 22, font)
        region_label.set_text_resize(res_hor=True, padding=4)
        region_label.set_transparent(True)
        self.add_widget(region_label, "region_label")

        # Level difficulty
        diff_label = MSGUI.Label(8, 34, 0, 22, font)
        diff_label.set_text_resize(res_hor=True, padding=4)
        diff_label.set_transparent(True)
        self.add_widget(diff_label, "diff_label")

        # Capture terrain (begin level) button
        capture_button = MSGUI.Button(8, height - 28, width - 8, 24, font, "Capture")
        capture_button.set_border(True)
        capture_button.set_hovered_color((150, 150, 150, 100))
        capture_button.set_pressed_color((100, 100, 100, 150))
        self.add_widget(capture_button, "capture_button")