import pygame
import MGUI


class GameFinishMSG(MGUI.WidgetCollection):
    def __init__(self, x, y):
        super().__init__()

        width = 264
        height = 128

        backg_widget = MGUI.Widget(x - width / 2, y - height / 2, width, height)
        backg_widget.set_background((60, 20, 60))
        backg_widget.set_border(True, (150, 20, 150))
        self.add_widget(backg_widget, "background", layer=13)

        font_16 = pygame.font.Font("assets/Dosis.otf", 16)
        font_21 = pygame.font.Font("assets/Dosis.otf", 21)
        font_42 = pygame.font.Font("assets/Dosis.otf", 42)

        tmp_x, tmp_y = backg_widget.get_position()

        # Finish message label
        finish_msg_label = MGUI.Label(tmp_x + 2, tmp_y + 2, backg_widget.get_width() - 4, 0, font_42)
        finish_msg_label.set_text_resize(res_ver=True, padding=4)
        finish_msg_label.set_transparent(True)
        finish_msg_label.set_font_color((255, 100, 255))
        self.add_widget(finish_msg_label, "finish_msg_label", layer=14)

        tmp_y += finish_msg_label.get_height()
        # Extra message
        extra_msg_label = MGUI.Label(tmp_x + 2, tmp_y, backg_widget.get_width() - 4, 0, font_16)
        extra_msg_label.set_text_resize(res_ver=True)
        extra_msg_label.set_transparent(True)
        self.add_widget(extra_msg_label, "extra_msg_label", layer=14)

        tmp_y = y + height / 2 - 37
        # Continue button
        continue_button = MGUI.Button(0, 0, 0, 25, font_21, "Continue")
        continue_button.set_text_resize(res_hor=True, padding=6)
        continue_button.set_position(x - continue_button.get_width() / 2, tmp_y)
        continue_button.set_border(True, (255, 100, 255))
        continue_button.set_hovered_color((150, 50, 150, 100))
        continue_button.set_pressed_color((100, 20, 100, 150))
        self.add_widget(continue_button, "continue_button", layer=14)

    def set_finish_message(self, msg):
        self["finish_msg_label"].set_text(msg)

    def set_extra_message(self, msg):
        self["extra_msg_label"].set_text(msg)