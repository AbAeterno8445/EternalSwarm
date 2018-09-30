import MGUI
import math

# Building types
buildtype_spawner = "spawner"
buildtype_support = "support"


class Building(MGUI.ImageWidget):
    def __init__(self, x, y, player_owned, building_data=None):
        super().__init__(8 + x * 48, 8 + y * 48, 48, 48)
        self.set_transparent(True)
        self.x = x
        self.y = y
        self.type = ""
        self.player_owned = player_owned

        if building_data:
            self.load_building(building_data)

    def load_building(self, building_data):
        for attr in building_data:
            if attr == "base_img":
                self.set_icon("assets/buildings/" + building_data[attr])
            elif hasattr(self, attr):
                setattr(self, attr, building_data[attr])

    def get_draw_position(self):
        return 8 + self.x * 48, 8 + self.y * 48

    def tick(self):
        pass


class BuildingTimedEffect(Building):
    """
    Buildings that produce an effect after a delayed time. Includes a progress bar.
    """
    def __init__(self, x, y, player_owned, building_data=None):
        self.effect_time = 0
        self.effect_ticker = 0
        super().__init__(x, y, player_owned, building_data)

    def tick(self):
        if self.effect_ticker < self.effect_time:
            self.effect_ticker += 1
        else:
            self.effect()

    def reset_ticker(self):
        self.effect_ticker = 0

    def effect(self):
        pass


class BuildingSpawner(BuildingTimedEffect):
    """
    Unit spawning buildings.
    """
    def __init__(self, x, y, player_owned, building_data=None):
        # Variables in building json
        self.spawn_unit = None
        super().__init__(x, y, player_owned, building_data)

        # Post-init variables
        self.spawn_ready = False

    def load_building(self, building_data):
        super().load_building(building_data)
        self.effect_time = math.ceil(building_data["spawn_time"] * 60)
        self.effect_ticker = 0

    def effect(self):
        self.spawn_ready = True

    def is_unit_ready(self):
        return self.spawn_ready

    def reset_spawn(self):
        self.spawn_ready = False
        self.reset_ticker()