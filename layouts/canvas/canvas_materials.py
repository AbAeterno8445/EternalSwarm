import pygame
import MGUI
from .cvswitcher import CanvasSwitcher


class CanvasMaterials(CanvasSwitcher):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (40, 0, 40))

        self.backg_widget.set_border(True, (160, 40, 160))

        font_18 = pygame.font.Font("assets/Dosis.otf", 18)
        font_12 = pygame.font.Font("assets/Dosis.otf", 12)
        # Player name
        self.plname_label = MGUI.Label(8, 8, self.get_width() - 16, 24, font_18)
        self.plname_label.set_background((15, 0, 15))
        self.plname_label.set_border(True, self.backg_widget.get_border_color())
        self.plname_label.set_font_color((255, 200, 255))
        self.add_element(self.plname_label)

        # Crystal image
        self.crystal_button = MGUI.ImageWidget(8, 40, 64, 64, "assets/materials/carbcrystal.png")
        self.crystal_button.set_icon_autoscale(True)
        self.add_element(self.crystal_button)

        tmp_width = self.get_width() - 68
        # Crystal amount number label
        self.crystal_amt_text = MGUI.Label(68, 40, tmp_width, 22, font_18, "0")
        self.crystal_amt_text.set_transparent(True)
        self.add_element(self.crystal_amt_text)

        # "Carbonic crystals" label
        self.crystal_text = MGUI.Label(68, 62, tmp_width, 22, font_18, "Carbonic crystals")
        self.crystal_text.set_transparent(True)
        self.add_element(self.crystal_text)

        # Crystals per second label
        self.ccps_text = MGUI.Label(68, 84, tmp_width, 22, font_12, "0 CCps")
        self.ccps_text.set_transparent(True)
        self.add_element(self.ccps_text)

    def update_data(self, player_data):
        self.plname_label.set_text(player_data.name)
        self.crystal_amt_text.set_text(player_data.get_carbcrystals_str())
        self.ccps_text.set_text(player_data.get_ccps_str() + " CCps")