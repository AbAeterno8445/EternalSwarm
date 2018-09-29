import MSGUI
import json
from level_map import LevelMap
from map_collection import MapCollection
import level_building as buildings


class CanvasGame(MSGUI.GUICanvas):
    def __init__(self, x, y, width, height, player_data):
        super().__init__(x, y, width, height)
        self.player_data = player_data

        # Load base buildings/units
        with open("assets/buildings.json", "r") as file:
            self.base_buildings = json.loads(file.read())
        with open("assets/units.json", "r") as file:
            self.base_units = json.loads(file.read())

        self.backg_widget.set_border(True, (200, 200, 200))

        self.levelmap = LevelMap(0, 0, 12, 8)
        self.levelmap.set_visible(False)

        self.map_coll = MapCollection(x, y, width, height, self.levelmap)
        self.add_element(self.map_coll.get_widgets_list())

        self.building_list = []
        self.units_list = []
        self.create_building_at(2, 3, "Slime Spawner")
        self.create_building_at(10, 4, "Slime Spawner")

    def create_building_at(self, x, y, building_name):
        new_building = self.base_buildings[building_name]
        tmp_building = None
        if "type" in new_building:
            # Create building based on type
            b_type = new_building["type"]

            # Unit spawner
            if b_type == buildings.buildtype_spawner:
                tmp_building = buildings.BuildingSpawner(x, y, new_building)
                # Set unit
                tmp_building.set_spawn_unit(self.base_units[tmp_building.spawn_unit])

        if not tmp_building:
            tmp_building = buildings.Building(x, y, new_building)

        self.building_list.append(tmp_building)
        self.add_element(tmp_building)

    def init_data(self, src_tile):
        self.levelmap.load_level(src_tile.region.name, src_tile.level_id)
        self.levelmap.set_visible(True)

    def tick(self):
        pass

    def handle_event(self, event_list):
        super().handle_event(event_list)

        self.map_coll.handle_event(event_list)
        self.map_coll.update()

        # Update buildings
        cam_x, cam_y = self.map_coll.get_camera_position()
        for b in self.building_list:
            b_drawx, b_drawy = b.get_draw_position()
            if not b.get_position() == (cam_x + b_drawx, cam_y + b_drawy):
                b.set_position(cam_x + b_drawx, cam_y + b_drawy)