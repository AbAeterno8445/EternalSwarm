from .screen import Screen
import layouts


class ScreenMain(Screen):
    def __init__(self, display, player_data):
        super().__init__(display)
        self.player_data = player_data
        disp_w, disp_h = display.get_size()

        # Materials canvas
        self.cv_materials = layouts.CanvasMaterials(16, 16, 200, disp_h - 100)

        # Main canvases
        tmp_x = self.cv_materials.get_width() + 32
        tmp_width = disp_w - tmp_x - 16
        self.cv_terrain = layouts.CanvasTerrain(tmp_x, 16, tmp_width, disp_h - 100)
        self.cv_buildings = layouts.CanvasBuildings(tmp_x, 16, *self.cv_terrain.get_size())
        self.cv_savegame = layouts.CanvasSaveGame(tmp_x, 16, *self.cv_terrain.get_size())

        self.current_main_canvas = "terrain"
        self.cv_main = {
            "terrain": self.cv_terrain,
            "buildings": self.cv_buildings,
            "savegame": self.cv_savegame
        }

        # Shortcuts canvas
        tmp_y = self.cv_terrain.get_height() + 24
        self.cv_shortcuts = layouts.CanvasShortcuts(tmp_x, tmp_y, tmp_width, 46)

        # Selected tile from terrain
        self.terrain_selected = None

        self.add_canvas([self.cv_materials, self.cv_shortcuts, self.cv_main[self.current_main_canvas]])

    def init_screen(self, source_screen=None):
        super().init_screen(source_screen)

        # Coming back from game, check if captured (victory)
        if isinstance(source_screen, layouts.ScreenGame):
            if source_screen.victory:
                capt_tile = source_screen.level_tile
                self.cv_main["terrain"].gamemap.capture_tile(capt_tile.x, capt_tile.y)
                self.cv_main["terrain"].select_tile(capt_tile)

    def update(self, event_list):
        self.terrain_selected = self.cv_terrain.map_coll.selected_tile
        self.cv_materials.update_data(self.player_data)
        return super().update(event_list)

    def check_switch(self, canvas):
        sw = canvas.get_switch()
        if sw in self.cv_main:
            self.remove_canvas(self.cv_main[self.current_main_canvas])
            self.current_main_canvas = sw
            self.add_canvas(self.cv_main[self.current_main_canvas])
        else:
            self.switch_screen = sw