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
    player_data.ccps = 3453

    # Init all canvas
    cv_materials = layouts.CanvasMaterials(16, 16, 200, 500)

    tmp_x = cv_materials.get_width() + 32
    tmp_width = disp_w - tmp_x - 16
    cv_main = layouts.CanvasMain(tmp_x, 16, tmp_width, 500)

    tmp_y = cv_main.get_height() + 24
    cv_shortcuts = layouts.CanvasShortcuts(tmp_x, tmp_y, tmp_width, 46)
    cv_list = (cv_materials, cv_main, cv_shortcuts)

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