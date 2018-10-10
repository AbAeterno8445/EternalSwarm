import pygame
import MGUI
from .cvswitcher import CanvasSwitcher


class CanvasSaveGame(CanvasSwitcher):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (70, 25, 0))

        self.backg_widget.set_border(True, (204, 102, 0))

        font_16 = pygame.font.Font("assets/Dosis.otf", 16)
        font_21 = pygame.font.Font("assets/Dosis.otf", 21)
        font_36 = pygame.font.Font("assets/Dosis.otf", 36)

        # Title
        self.title_label = MGUI.Label(0, 0, 0, 0, font_36, "Save Game")
        self.title_label.set_text_resize(res_hor=True, res_ver=True, padding=8)
        self.title_label.set_position(width / 2 - self.title_label.get_width() / 2, 4)
        self.title_label.set_transparent(True)
        self.title_label.set_font_color((255, 122, 0))
        self.add_element(self.title_label)

        tmp_x = 16
        tmp_y = 80
        # Save name label
        self.savename_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_21, "Save name:")
        self.savename_label.set_text_resize(res_hor=True, res_ver=True, padding=4)
        self.savename_label.set_transparent(True)
        self.savename_label.set_font_color((255, 122, 0))
        self.add_element(self.savename_label)

        save_button_w = 80
        tmp_y += self.savename_label.get_height() + 4
        # Save name input
        self.savename_input = MGUI.InputBox(tmp_x, tmp_y, width - 32 - save_button_w, 28, font_16)
        self.savename_input.set_border(True, (255, 122, 0))
        self.savename_input.set_selected_bordercolor((255, 255, 0))
        self.savename_input.set_character_limit(30)
        self.savename_input.set_forbidden_characters("./\\\"<>'")
        self.add_element(self.savename_input)

        tmp_x += self.savename_input.get_width() + 4
        # Save button
        self.save_button = MGUI.Button(tmp_x, tmp_y, save_button_w, self.savename_input.get_height(), font_16, "Save")
        self.save_button.set_border(True, (255, 122, 0))
        self.save_button.set_font_color((255, 122, 0))
        self.save_button.set_hovered_color((100, 100, 100, 80))
        self.save_button.set_pressed_color((100, 100, 100, 150))
        self.add_element(self.save_button)

        tmp_x = 16
        tmp_y += self.savename_input.get_height() + 4
        # Existing saves label
        self.exsaves_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_21, "Existing saves:")
        self.exsaves_label.set_text_resize(res_hor=True, res_ver=True, padding=4)
        self.exsaves_label.set_transparent(True)
        self.exsaves_label.set_font_color((255, 122, 0))
        self.add_element(self.exsaves_label)

        tmp_y += self.savename_input.get_height() + 4
        # Existing saves box
        self.exsaves_backg = MGUI.Widget(tmp_x, tmp_y, width - 32, height - tmp_y - 16)
        self.exsaves_backg.set_border(True, (255, 122, 0))
        self.add_element(self.exsaves_backg)