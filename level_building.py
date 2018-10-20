import MGUI
import math
from level_unit import HealthHandler

# Building types
buildtype_spawner = "spawner"
buildtype_support = "support"


class Building(MGUI.ImageWidget, HealthHandler):
    def __init__(self, x, y, player_owned, building_data=None):
        MGUI.ImageWidget.__init__(self, 8 + x * 48, 8 + y * 48, 48, 48)
        HealthHandler.__init__(self)
        self.set_transparent(True)
        self.x = x
        self.y = y
        self.type = ""
        self.map_color = (255, 0, 0)
        self.cost = 0
        self.player_owned = player_owned

        if building_data:
            self.load_building(building_data)

        self.healthbar = MGUI.Healthbar(4, self.get_height() - 8, 40, 4)
        self.healthbar.set_background((20, 20, 20))
        self.healthbar.set_color((50, 255, 50))

    def load_building(self, building_data):
        for attr in building_data:
            if attr == "base_img":
                self.set_icon("assets/buildings/" + building_data[attr])
            elif hasattr(self, attr):
                setattr(self, attr, building_data[attr])

        self.hp = self.maxhp

    def get_draw_position(self):
        return 8 + self.x * 48, 8 + self.y * 48

    def hurt(self, dmg_dict):
        super().hurt(dmg_dict)
        self.mark_dirty()

    def tick(self):
        # Handle healthbar
        if 0 < self.hp < self.maxhp:
            self.healthbar.set_visible(True)
            perc = self.hp / self.maxhp
            self.healthbar.set_percentage(perc)

            # Color (green when healthy, red when damaged)
            col_perc = math.floor(205 * (1 - perc))
            col_r = 50 + col_perc
            col_g = 255 - col_perc
            self.healthbar.set_color((col_r, col_g, 50))
        else:
            if self.healthbar.is_visible():
                self.healthbar.set_visible(False)
                self.mark_dirty()

    def _get_appearance(self, *args):
        surface = super()._get_appearance(*args)
        if self.healthbar.is_visible():
            surface.blit(self.healthbar._get_appearance(*args), self.healthbar.get_position())
        return surface


class BuildingTimedEffect(Building):
    """
    Buildings that produce an effect after a delayed time. Includes a progress bar.
    """
    def __init__(self, x, y, player_owned, building_data=None):
        self.effect_bar = MGUI.Healthbar(4, 4, 40, 4)
        self.effect_bar.set_background((20, 20, 20))
        self.effect_bar.set_color((150, 50, 150))

        self.effect_time = 0
        self.effect_ticker = 0
        super().__init__(x, y, player_owned, building_data)

    def update_effect_bar(self):
        if self.effect_time > 0 and self.effect_ticker > 0:
            self.effect_bar.set_percentage(self.effect_ticker / self.effect_time)
        else:
            self.effect_bar.set_percentage(0)
        self.mark_dirty()

    def tick(self):
        super().tick()
        if self.effect_ticker < self.effect_time:
            self.effect_ticker += 1
        else:
            self.effect()
        self.update_effect_bar()

    def reset_ticker(self):
        self.effect_ticker = 0

    def effect(self):
        pass

    def _get_appearance(self, *args):
        surface = super()._get_appearance(*args)
        surface.blit(self.effect_bar._get_appearance(*args), self.effect_bar.get_position())
        return surface


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
        self.update_effect_bar()

    def effect(self):
        self.spawn_ready = True

    def is_unit_ready(self):
        return self.spawn_ready

    def reset_spawn(self):
        self.spawn_ready = False
        self.reset_ticker()