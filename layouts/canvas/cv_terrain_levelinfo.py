import pygame
import MGUI


class TerrainLevelinfo(MGUI.WidgetCollection):
    def __init__(self, x, y, width, height):
        super().__init__()

        backg_widget = MGUI.Widget(x, y, width, height)
        backg_widget.set_background((20, 20, 20, 150))
        backg_widget.set_border(True)
        self.add_widget(backg_widget, "background", layer=2)

        font = pygame.font.Font("assets/Dosis.otf", 18)
        # Region name
        region_label = MGUI.Label(8, 8, 0, 22, font)
        region_label.set_text_resize(res_hor=True, padding=4)
        region_label.set_transparent(True)
        self.add_widget(region_label, "region_label", layer=3)

        # Capture terrain (jump to terrain info screen) button
        capture_button = MGUI.Button(8, height - 28, width - 8, 24, font, "Capture")
        capture_button.set_border(True)
        capture_button.set_hovered_color((150, 150, 150, 100))
        capture_button.set_pressed_color((100, 100, 100, 150))
        self.add_widget(capture_button, "capture_button", layer=3)

        # Owned terrain label
        level_info_label = MGUI.Label(8, height - 28, width - 8, 24, font, "Owned")
        level_info_label.set_transparent(True)
        level_info_label.set_visible(False)
        self.add_widget(level_info_label, "level_info_label", layer=3)

    def update_data(self, selected_tile):
        self["region_label"].set_text(selected_tile.region.name)

        if selected_tile.owned:
            # Tile owned - deactivate capture button and activate info label
            self.set_widget_visible("capture_button", False)
            self["capture_button"].set_active(False)

            self["level_info_label"].set_text("Owned")
            self.set_widget_visible("level_info_label", True)
        elif selected_tile.capturable:
            # Capturable tile - activate capture button and deactivate info label
            self.set_widget_visible("capture_button", True)
            self["capture_button"].set_active(True)

            self.set_widget_visible("level_info_label", False)
        else:
            # Non-capturable tile - deactivate capture button, change and activate info label
            self.set_widget_visible("capture_button", False)
            self["capture_button"].set_active(False)

            self["level_info_label"].set_text("Not capturable")
            self.set_widget_visible("level_info_label", True)