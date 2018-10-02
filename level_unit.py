import MGUI


class Unit(MGUI.AnimSprite):
    def __init__(self, x, y, player_owned, unit_data=None):
        super().__init__(x, y, 1, 1)
        self.draw_x = x
        self.draw_y = y
        self.speed = 0
        self.player_owned = player_owned

        if unit_data:
            self.load_unit(unit_data)

    def load_unit(self, unit_data):
        for attr in unit_data:
            if attr == "img_data":  # Load animated sprite data
                anim_data = unit_data[attr]
                self.set_icon_animated("assets/units/" + anim_data["img"], anim_data["frames"])
                if "anim_delay" in anim_data:
                    self.set_animation_delay(anim_data["anim_delay"])
                if "anim_order" in anim_data:
                    self.set_animation_order(anim_data["anim_order"])
                if "rotate" in anim_data:
                    self.set_rotation(anim_data["rotate"])
                flip_hor = "flip_hor" in anim_data and self.player_owned or not self.player_owned  # Flip enemy units
                flip_ver = "flip_ver" in anim_data
                if flip_hor or flip_ver:
                    self.set_flip(flip_hor, flip_ver)
            elif hasattr(self, attr):
                setattr(self, attr, unit_data[attr])

    def set_draw_position(self, x, y):
        self.draw_x = x
        self.draw_y = y

    def get_draw_position(self):
        return self.draw_x, self.draw_y

    def tick(self):
        mx, my = self.get_draw_position()
        if self.player_owned:
            mx += self.speed
        else:
            mx -= self.speed
        self.set_draw_position(mx, my)