import pygame
from pygame.locals import DOUBLEBUF
from playerdata import PlayerData
import layouts


def main():
    # Init display & clock
    display = pygame.display.set_mode((800, 600), DOUBLEBUF)
    disp_w, disp_h = display.get_size()
    pygame.display.set_caption("Eternal Swarm")
    display_icon = pygame.transform.scale(pygame.image.load("assets/materials/sapphire.png"), (64, 64))
    pygame.display.set_icon(display_icon)
    clock = pygame.time.Clock()

    # Player data holder
    player_data = PlayerData("Player")

    # Init all canvas
    game_running = False
    cv_game = layouts.CanvasGame(0, 0, disp_w, disp_h, player_data)

    cv_materials = layouts.CanvasMaterials(16, 16, 200, disp_h - 100)

    # Main canvas variations and dictionary
    tmp_x = cv_materials.get_width() + 32
    tmp_width = disp_w - tmp_x - 16
    cv_terrain = layouts.CanvasTerrain(tmp_x, 16, tmp_width, disp_h - 100)
    cv_levelinfo = layouts.CanvasLevelInfo(tmp_x, 16, *cv_terrain.get_size())
    cv_buildings = layouts.CanvasBuildings(tmp_x, 16, *cv_terrain.get_size())

    current_main_canvas = "terrain"
    cv_main = {
        "terrain": cv_terrain,
        "terrain_lvlinfo": cv_levelinfo,
        "buildings": cv_buildings
    }

    tmp_y = cv_terrain.get_height() + 24
    cv_shortcuts = layouts.CanvasShortcuts(tmp_x, tmp_y, tmp_width, 46)
    cv_list = (cv_materials, cv_shortcuts)

    frame = 0
    loop = True
    while loop:
        caught_events = pygame.event.get()
        for event in caught_events:
            if event.type == pygame.QUIT:
                loop = False
                break

        frame = (frame + 1) % 60

        if frame % 5 == 0:
            player_data.ccps_tick(12)
            cv_materials.update_data(player_data)

        upd_rects = []
        # Draw game canvas while playing, menu canvases otherwise
        if game_running:
            cv_game.handle_event(caught_events)
            upd_rects += cv_game.draw(display)
        else:
            # Draw main canvas
            cur_canvas = cv_main[current_main_canvas]
            cur_canvas.handle_event(caught_events)
            upd_rects += cur_canvas.draw(display)

            switch_cv = cur_canvas.get_switch_canvas()
            if switch_cv:
                # Switch main canvas
                if switch_cv in cv_main:
                    current_main_canvas = switch_cv
                    cv_main[current_main_canvas].backg_widget.mark_dirty()

            if isinstance(cur_canvas, layouts.CanvasTerrain):
                if cur_canvas.start_game:
                    cv_game.init_data(cur_canvas.map_coll.selected_tile)
                    cur_canvas.start_game = False
                    game_running = True
            # Draw other canvases
            for canvas in cv_list:
                canvas.handle_event(caught_events)
                upd_rects += canvas.draw(display)

        pygame.display.update(upd_rects)
        clock.tick(60)


if __name__ == '__main__':
    pygame.display.init()
    pygame.font.init()
    main()
    pygame.quit()