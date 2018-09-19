import pygame
from pygame.locals import DOUBLEBUF
from playerdata import PlayerData
import layouts


def main():
    # Init display
    display = pygame.display.set_mode((800, 600), DOUBLEBUF)
    pygame.display.set_caption("Eternal Swarm")
    clock = pygame.time.Clock()

    player_data = PlayerData("Player")

    canvas_materials = layouts.create_canvas_materials()
    canvas_main = layouts.create_canvas_main()
    canvas_list = (canvas_materials, canvas_main)

    loop = True
    while loop:
        caught_events = pygame.event.get()
        for event in caught_events:
            if event.type == pygame.QUIT:
                loop = False
                break

        upd_rects = []
        for canvas in canvas_list:
            canvas.handle_event(caught_events)
            upd_rects += canvas.draw(display)
        pygame.display.update(upd_rects)
        clock.tick(60)


if __name__ == '__main__':
    pygame.display.init()
    pygame.font.init()
    main()
    pygame.quit()