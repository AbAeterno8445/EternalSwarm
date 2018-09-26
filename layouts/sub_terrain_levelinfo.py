import pygame
import MSGUI


class TerrainLevelinfo(MSGUI.WidgetCollection):
    def __init__(self, x, y, width, height):
        super().__init__()

        backg_widget = MSGUI.Widget(x, y, width, height)
        backg_widget.set_background((20, 20, 20, 150))
        backg_widget.set_border(True)
        self.add_widget(backg_widget, "background", layer=0)

        font = pygame.font.Font("assets/Dosis.otf", 18)
        # Region name
        region_label = MSGUI.Label(8, 8, 0, 22, font)
        region_label.set_text_resize(res_hor=True, padding=4)
        region_label.set_transparent(True)
        self.add_widget(region_label, "region_label", layer=1)

        # Level difficulty
        diff_label = MSGUI.Label(8, 34, 0, 22, font)
        diff_label.set_text_resize(res_hor=True, padding=4)
        diff_label.set_transparent(True)
        self.add_widget(diff_label, "diff_label", layer=1)

        # Capture terrain (begin level) button
        capture_button = MSGUI.Button(8, height - 28, width - 8, 24, font, "Capture")
        capture_button.set_border(True)
        capture_button.set_hovered_color((150, 150, 150, 100))
        capture_button.set_pressed_color((100, 100, 100, 150))
        self.add_widget(capture_button, "capture_button", layer=1)

        # Owned terrain label
        owned_label = MSGUI.Label(8, height - 28, width - 8, 24, font, "Owned")
        owned_label.set_transparent(True)
        owned_label.set_visible(False)
        self.add_widget(owned_label, "owned_label", layer=1)

    def update_data(self, selected_tile, region):
        self["region_label"].set_text(region.name)
        self["diff_label"].set_text("Diff: " + str(selected_tile.difficulty))

        if selected_tile.owned:
            self.set_widget_visible("capture_button", False)
            self["capture_button"].set_active(False)
            self.set_widget_visible("owned_label", True)
        else:
            self.set_widget_visible("capture_button", True)
            self["capture_button"].set_active(True)
            self.set_widget_visible("owned_label", False)