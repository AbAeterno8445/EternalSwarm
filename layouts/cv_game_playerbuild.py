import pygame
import MGUI
from millify import millify_num


class PlayerBuildMenu(MGUI.WidgetCollection):
    def __init__(self, x, y, width, height, base_buildings, player_data, place_building_method):
        super().__init__()

        self.base_buildings = base_buildings

        backg_widget = MGUI.Widget(x, y, width, height)
        backg_widget.set_background((60, 20, 60, 150))
        backg_widget.set_border(True, (150, 20, 150))
        self.add_widget(backg_widget, "background", layer=2)

        font_22 = pygame.font.Font("assets/Dosis.otf", 22)
        font_16 = pygame.font.Font("assets/Dosis.otf", 16)
        build_label = MGUI.Label(x + 4, y + 4, width - 8, 0, font_22, "Build...")
        build_label.set_text_resize(res_ver=True, padding=4)
        build_label.set_background((60, 20, 60, 255))
        build_label.set_border(True, backg_widget.get_border_color())
        self.add_widget(build_label, "build_label", layer=3)

        # Building buttons
        button_start_y = build_label.get_position()[1] + build_label.get_height() + 4
        button_height = 64
        self.building_buttons = []
        for i, bname in enumerate(player_data.owned_buildings):
            self.building_buttons.append(bname)
            bdata = self.base_buildings[bname]

            button_x = x + 4
            button_y = button_start_y + 68 * i

            # Background
            tmp_bg = MGUI.Widget(button_x, button_y, width - 8, button_height)
            tmp_bg.set_background((80, 0, 80))
            tmp_bg.set_border(True, (150, 0, 150))
            self.add_widget(tmp_bg, "button_" + bname + "_bg", layer=3)

            # Image
            tmp_img = MGUI.ImageWidget(button_x, button_y, button_height, button_height, "assets/buildings/" + bdata["base_img"])
            tmp_img.set_border(True, tmp_bg.get_border_color())
            self.add_widget(tmp_img, "button_" + bname + "_img", layer=4)

            tmp_x = button_x + tmp_img.get_width() - 1
            tmp_width = tmp_bg.get_width() - tmp_img.get_width() + 1
            # Name label
            tmp_name_label = MGUI.Label(tmp_x, button_y, tmp_width, 0, font_16, bname)
            tmp_name_label.set_text_resize(res_ver=True)
            tmp_name_label.set_background(tmp_bg.get_background())
            tmp_name_label.set_border(True, tmp_bg.get_border_color())
            self.add_widget(tmp_name_label, "button_" + bname + "_namelabel", layer=4)

            tmp_y = button_y + tmp_name_label.get_height()
            tmp_height = tmp_bg.get_height() - tmp_name_label.get_height() - 2
            cost_img_width = 18
            # Cost label & img
            tmp_cost_label = MGUI.Label(0, 0, 0, tmp_height, font_16, "Cost: " + millify_num(bdata["cost"]))
            tmp_cost_label.set_text_resize(res_hor=True, padding=4)
            tmp_x += 1 + tmp_width / 2 - (tmp_cost_label.get_width() + cost_img_width) / 2
            tmp_y += 1
            tmp_cost_label.set_position(tmp_x, tmp_y)
            tmp_cost_label.set_background(tmp_bg.get_background())
            self.add_widget(tmp_cost_label, "button_" + bname + "_costlabel", layer=4)

            tmp_x += tmp_cost_label.get_width()
            tmp_cost_img = MGUI.AnimSprite(tmp_x, tmp_y, cost_img_width, tmp_height, "assets/materials/energy.png", 4, autosize=False)
            tmp_cost_img.set_icon_autoscale(False)
            self.add_widget(tmp_cost_img, "button_" + bname + "_costimg", layer=4)

            # Place building button
            tmp_place_button = MGUI.Button(button_x, button_y + button_height, tmp_bg.get_width(), 22, font_16, "Place building")
            tmp_place_button.set_callback(place_building_method, [bname])
            tmp_place_button.set_background(tmp_bg.get_background())
            tmp_place_button.set_border(True, tmp_bg.get_border_color())
            tmp_place_button.set_hovered_color((150, 0, 150, 100))
            tmp_place_button.set_pressed_color((70, 0, 70, 100))
            self.add_widget(tmp_place_button, "button_" + bname + "_place", layer=4)

    # Update buttons
    def update_data(self, energy):
        for bname in self.building_buttons:
            # Check if affordable
            tmp_place_button = self["button_" + bname + "_place"]
            if energy < self.base_buildings[bname]["cost"]:
                if tmp_place_button.is_active():
                    tmp_place_button.set_active(False)
            else:
                if not tmp_place_button.is_active():
                    tmp_place_button.set_active(True)