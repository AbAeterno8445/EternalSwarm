import MSGUI
from level_map import LevelMap
from map_collection import MapCollection


class CanvasGame(MSGUI.GUICanvas):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.backg_widget.set_border(True, (200, 200, 200))

        self.levelmap = LevelMap(0, 0, 12, 8)
        self.levelmap.set_visible(False)

        self.map_coll = MapCollection(x, y, width, height, self.levelmap)
        self.add_element(self.map_coll.get_widgets_list())

    def init_data(self, src_tile):
        self.levelmap.load_level(src_tile.region.name, src_tile.level_id)
        self.levelmap.set_visible(True)

    def handle_event(self, event_list):
        super().handle_event(event_list)

        self.map_coll.handle_event(event_list)
        self.map_coll.update()