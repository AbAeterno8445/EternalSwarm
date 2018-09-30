import MGUI
from level_unit import Unit

# Building types
buildtype_spawner = "spawner"
buildtype_support = "support"


class Building(MGUI.Widget):
    def __init__(self, x, y, building_data=None):
        super().__init__(8 + x * 48, 8 + y * 48, 48, 48)
        self.set_transparent(True)
        self.x = x
        self.y = y
        self.base_img = MGUI.ImageWidget(0, 0, 48, 48)

        if building_data:
            self.load_building(building_data)

    def load_building(self, building_data):
        for attr in building_data:
            if attr == "base_img":
                self.base_img.set_icon("assets/buildings/" + building_data[attr])
            elif hasattr(self, attr):
                setattr(self, attr, building_data[attr])

    def get_draw_position(self):
        return 8 + self.x * 48, 8 + self.y * 48

    def _get_appearance(self, *args):
        surface = super()._get_appearance(*args)
        surface.blit(self.base_img._get_appearance(*args), (0, 0))
        return surface


class BuildingSpawner(Building):
    def __init__(self, x, y, building_data=None):
        self.spawn_time = 0
        self.spawn_ticker = 0
        self.spawn_unit = None

        super().__init__(x, y, building_data)

    def update(self):
        super().update()
        if self.spawn_ticker > 0:
            self.spawn_ticker -= 1
        # else:
        #     self.spawn_ticker = self.spawn_time