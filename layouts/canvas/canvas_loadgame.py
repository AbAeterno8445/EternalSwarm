import pygame
import MGUI
import json
import os
import math
from .cvswitcher import CanvasSwitcher
from millify import millify_num


class CanvasLoadGame(CanvasSwitcher):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, (70, 25, 0))

        self.load_objs = {}
        self.selected_button = None
        self.load_metadata = {}

        self.backg_widget.set_border(True, (204, 102, 0))

        font_16 = pygame.font.Font("assets/Dosis.otf", 16)
        font_21 = pygame.font.Font("assets/Dosis.otf", 21)
        font_36 = pygame.font.Font("assets/Dosis.otf", 36)

        # Title
        self.title_label = MGUI.Label(0, 0, 0, 0, font_36, "Load Game")
        self.title_label.set_text_resize(res_hor=True, res_ver=True, padding=8)
        self.title_label.set_position(width / 2 - self.title_label.get_width() / 2, 4)
        self.title_label.set_transparent(True)
        self.title_label.set_font_color((255, 122, 0))
        self.add_element(self.title_label)

        tmp_x = 16
        tmp_y = 80
        # Load game label
        self.loadgame_label = MGUI.Label(tmp_x, tmp_y, 0, 0, font_21, "Load game:")
        self.loadgame_label.set_text_resize(res_hor=True, res_ver=True, padding=4)
        self.loadgame_label.set_transparent(True)
        self.loadgame_label.set_font_color((255, 122, 0))
        self.add_element(self.loadgame_label)

        tmp_y += self.loadgame_label.get_height() + 4
        # Existing games box
        self.exgames_backg = MGUI.Widget(tmp_x, tmp_y, width / 2 - 20, height - tmp_y - 16)
        self.exgames_backg.set_border(True, (255, 122, 0))
        self.add_element(self.exgames_backg)

        # Load button handling variables
        self.load_buttons = []
        self.load_buttons_pad = 0
        self.load_buttons_limit = 13
        self.update_savefiles()

        tmp_x += self.exgames_backg.get_width() + 10
        # Load info background
        self.loadinfo_backg = MGUI.Widget(tmp_x, tmp_y, *self.exgames_backg.get_size())
        self.loadinfo_backg.set_border(True, (255, 122, 0))
        self.add_element(self.loadinfo_backg)

        tmp_x += 1
        tmp_y += 1
        # Load info label
        self.loadinfo_label = MGUI.Label(tmp_x, self.loadgame_label.get_position()[1], 0, 0, font_21, "Load info:")
        self.loadinfo_label.set_text_resize(res_hor=True, res_ver=True, padding=4)
        self.loadinfo_label.set_transparent(True)
        self.loadinfo_label.set_font_color((255, 122, 0))
        self.add_element(self.loadinfo_label)

        tmp_width = self.loadinfo_backg.get_width() - 2
        # Load name label
        self.loadname_label = MGUI.Label(tmp_x, tmp_y, tmp_width, 0, font_21)
        self.loadname_label.set_text_resize(res_ver=True)
        self.loadname_label.set_border(True, (255, 122, 0))
        self.loadname_label.set_transparent(True)
        self.add_element(self.loadname_label, layer=1)

        tmp_y += self.loadname_label.get_height() + 6
        # Load time label
        self.loadtime_label = MGUI.Label(tmp_x, tmp_y, tmp_width, 0, font_16)
        self.loadtime_label.set_text_resize(res_ver=True)
        self.loadtime_label.set_transparent(True)
        self.add_element(self.loadtime_label, layer=1)

        tmp_y += self.loadtime_label.get_height() + 2
        # Player name label
        self.loadplname_label = MGUI.Label(tmp_x, tmp_y, tmp_width, 0, font_16)
        self.loadplname_label.set_text_resize(res_ver=True)
        self.loadplname_label.set_transparent(True)
        self.add_element(self.loadplname_label, layer=1)

        tmp_y += self.loadplname_label.get_height() + 2
        # Carbonic crystals label
        self.loadcrystals_label = MGUI.Label(tmp_x, tmp_y, tmp_width, 0, font_16)
        self.loadcrystals_label.set_text_resize(res_ver=True)
        self.loadcrystals_label.set_transparent(True)
        self.add_element(self.loadcrystals_label, layer=1)

        tmp_x += 8
        tmp_width -= 16
        # Load game button
        self.loadgame_button = MGUI.Button(0, 0, tmp_width, 0, font_21, "Load game")
        self.loadgame_button.set_text_resize(res_ver=True, padding=2)
        tmp_y = self.loadinfo_backg.get_position()[1] + self.loadinfo_backg.get_height() - self.loadgame_button.get_height() - 8
        self.loadgame_button.set_position(tmp_x, tmp_y)
        self.loadgame_button.set_border(True, (255, 122, 0))
        self.loadgame_button.set_font_color((255, 122, 0))
        self.loadgame_button.set_hovered_color((100, 100, 100, 80))
        self.loadgame_button.set_pressed_color((100, 100, 100, 150))
        self.loadgame_button.set_active(False)
        self.add_element(self.loadgame_button, layer=1)

    def on_switch(self):
        self.selected_button = None
        self.update_load_data()
        self.update_savefiles()

    # load_obj must be an object with the 'json_load' method
    # json_load must load a dictionary into the object's attributes
    def add_load_object(self, load_obj, obj_name):
        if hasattr(load_obj, "json_load"):
            self.load_objs[obj_name] = load_obj
        else:
            raise Exception("Load object " + str(type(load_obj)) + " is missing the json_load method.")

    def handle_event(self, event_list):
        super().handle_event(event_list)
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll down
                    self.scroll_buttons(-1)
                elif event.button == 5:  # Scroll up
                    self.scroll_buttons(1)

    def scroll_buttons(self, scroll):
        self.load_buttons_pad = max(0, min(len(self.load_buttons) - self.load_buttons_limit + 1, self.load_buttons_pad + scroll))

        for b in self.load_buttons:
            b.set_visible(False)

        loadbt_x, loadbt_y = self.exgames_backg.get_position()
        loadbt_x += 1
        loadbt_y += 1
        for i in range(self.load_buttons_pad, min(len(self.load_buttons), self.load_buttons_pad + self.load_buttons_limit - 1)):
            self.load_buttons[i].set_visible(True)
            self.load_buttons[i].set_position(loadbt_x, loadbt_y)
            loadbt_y += self.load_buttons[i].get_height()

    def select_load(self, button):
        if self.selected_button:
            self.selected_button.set_border(False)
        self.selected_button = button
        button.set_border(True)

        try:
            with open("saves/" + button.get_text() + ".issf", "r") as file:
                self.load_metadata = json.loads(file.read())["metadata"]
            self.update_load_data()
        except FileNotFoundError:
            self.selected_button = None
            self.remove_element(button)
            self.update_savefiles()
            return

    def update_load_data(self):
        if self.selected_button:
            self.loadname_label.set_text(self.selected_button.get_text())
            self.loadtime_label.set_text(self.load_metadata["time"])
            self.loadplname_label.set_text(self.load_metadata["player_name"])
            self.loadcrystals_label.set_text(millify_num(self.load_metadata["crystals"]) + " carbonic crystals")
            self.loadgame_button.set_callback(self.load_game, self.selected_button.get_text())
            self.loadgame_button.set_active(True)
        else:
            self.loadname_label.set_text("")
            self.loadtime_label.set_text("")
            self.loadplname_label.set_text("")
            self.loadcrystals_label.set_text("")
            self.loadgame_button.set_active(False)

    def load_game(self, name):
        with open("saves/" + name + ".issf", "r") as file:
            load_dict = json.loads(file.read())

        for data in load_dict:
            if data in self.load_objs:
                self.load_objs[data].json_load(load_dict[data])

    def update_savefiles(self):
        saves = sorted(os.listdir("saves"))

        for b in self.load_buttons:
            self.remove_element(b)
        self.load_buttons.clear()

        loadbt_x, loadbt_y = self.exgames_backg.get_position()
        loadbt_x += 1
        loadbt_y += 1
        font_16 = pygame.font.Font("assets/Dosis.otf", 16)
        but_height = font_16.size("A")[1]

        self.load_buttons_limit = math.floor(self.exgames_backg.get_height() / but_height)
        box_height = 0
        for s in saves:
            # Infinity Swarm Save File
            if len(s) > 5 and not s[-5:] == ".issf":
                continue

            load_button = MGUI.Button(loadbt_x, loadbt_y, self.exgames_backg.get_width() - 2, 0, font_16)
            load_button.set_text("%s" % s[:-5])
            load_button.set_callback(self.select_load, load_button)
            load_button.set_text_resize(res_ver=True, padding=1)
            load_button.set_hovered_color((100, 100, 100, 50))
            load_button.set_pressed_color((100, 100, 100, 120))
            self.load_buttons.append(load_button)
            self.add_element(load_button, layer=1)

            if len(self.load_buttons) >= self.load_buttons_limit:
                load_button.set_visible(False)
            else:
                box_height += load_button.get_height()

            loadbt_y += load_button.get_height()
        self.exgames_backg.set_bounds_size(self.exgames_backg.get_width(), max(self.exgames_backg.get_height(), box_height + 2))

        self.scroll_buttons(0)