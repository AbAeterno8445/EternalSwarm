import pygame
import MGUI
import os
import math
import json
from .cvswitcher import CanvasSwitcher


class CanvasSaveGame(CanvasSwitcher):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (70, 25, 0))

        self.save_data = {}

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
        self.save_button.set_callback(self.create_savefile)
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

        # Save button handling variables
        self.save_buttons = []
        self.save_buttons_pad = 0
        self.save_buttons_limit = 13
        self.update_savefiles()

    # save_obj must be an object with the 'json_save' method
    # json_save must return a dictionary with the object data
    def add_save_object(self, save_obj, obj_name):
        if hasattr(save_obj, "json_save"):
            self.save_data[obj_name] = save_obj
        else:
            raise Exception("Save object " + str(type(save_obj)) + " is missing the json_save method.")

    def handle_event(self, event_list):
        super().handle_event(event_list)
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll down
                    self.scroll_buttons(-1)
                elif event.button == 5:  # Scroll up
                    self.scroll_buttons(1)

    def create_savefile(self):
        save_name = self.savename_input.get_text().strip()
        save_dict = {}
        for s in self.save_data:
            save_dict[s] = self.save_data[s].json_save()
        if len(save_name) > 0:
            with open("saves/" + save_name + ".issf", "w") as file:
                file.write(json.dumps(save_dict, indent=2))
            self.update_savefiles()

    def scroll_buttons(self, scroll):
        self.save_buttons_pad = max(0, min(len(self.save_buttons) - self.save_buttons_limit + 1, self.save_buttons_pad + scroll))

        for b in self.save_buttons:
            b.set_visible(False)

        savebt_x, savebt_y = self.exsaves_backg.get_position()
        savebt_x += 1
        savebt_y += 1
        for i in range(self.save_buttons_pad, min(len(self.save_buttons), self.save_buttons_pad + self.save_buttons_limit - 1)):
            self.save_buttons[i].set_visible(True)
            self.save_buttons[i].set_position(savebt_x, savebt_y)
            savebt_y += self.save_buttons[i].get_height()

    def update_savefiles(self):
        saves = sorted(os.listdir("saves"))

        for b in self.save_buttons:
            self.remove_element(b)
        self.save_buttons.clear()

        savebt_x, savebt_y = self.exsaves_backg.get_position()
        savebt_x += 1
        savebt_y += 1
        font_16 = pygame.font.Font("assets/Dosis.otf", 16)
        but_height = font_16.size("a")[1]

        self.save_buttons_limit = math.floor(self.exsaves_backg.get_height() / but_height)
        for s in saves:
            # Infinity Swarm Save File
            if len(s) > 5 and not s[-5:] == ".issf":
                continue

            save_button = MGUI.Button(savebt_x, savebt_y, self.exsaves_backg.get_width() - 2, 0, font_16)
            save_button.set_text("%s" % s[:-5])
            save_button.set_callback(self.savename_input.set_text, [save_button.get_text()])
            save_button.set_text_resize(res_ver=True, padding=1)
            save_button.set_hovered_color((100, 100, 100, 50))
            save_button.set_pressed_color((100, 100, 100, 120))
            self.save_buttons.append(save_button)
            self.add_element(save_button, layer=1)

            if len(self.save_buttons) >= self.save_buttons_limit:
                save_button.set_visible(False)

            savebt_y += save_button.get_height()

        self.scroll_buttons(0)