import MGUI


class Unit(MGUI.AnimSprite):
    def __init__(self, x, y, unit_data=None):
        super().__init__(x, y, 1, 1)
        self.speed = 0
        self.x = x
        self.y = y

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
            elif hasattr(self, attr):
                setattr(self, attr, unit_data[attr])