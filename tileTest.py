import pygame
from pygame.locals import DOUBLEBUF
import MSGUI
from game_map import GameMap


def main():
    display = pygame.display.set_mode((800, 600), DOUBLEBUF)
    pygame.display.set_caption("MSGUI Tiling test")
    clock = pygame.time.Clock()

    canvas_1 = MSGUI.GUICanvas(0, 0, 400, 600, (0, 50, 50))
    gamemap_1 = GameMap(0, 0, 8, 8)
    gamemap_1.add_region_multiple([
        ("Grasslands", "assets/tiletest/tile_grass.png"),
        ("Hallow grasslands", "assets/tiletest/tile_hallow.png")
    ])
    canvas_1.add_element(gamemap_1, widget=True)

    canvas_2 = MSGUI.GUICanvas(400, 0, 400, 600, (50, 0, 50))
    gamemap_2 = GameMap(0, 0, 8, 8)
    gamemap_2.add_region_multiple([
        ("Gem1", "assets/tiletest/tile_gem1.png"),
        ("Gem2", "assets/tiletest/tile_gem2.png"),
        ("Gem3", "assets/tiletest/tile_gem3.png"),
        ("Gem4", "assets/tiletest/tile_gem4.png"),
        ("Gem5", "assets/tiletest/tile_gem5.png"),
        ("Gem6", "assets/tiletest/tile_gem6.png")
    ])
    canvas_2.add_element(gamemap_2, widget=True)

    canvas_list = [canvas_1, canvas_2]

    camera_x = display.get_width() / 2 - gamemap_1.width * 24
    camera_y = display.get_height() / 2 - gamemap_1.height * 24
    camera_drag = False
    camera_drag_x = 0
    camera_drag_y = 0

    gamemap_1.set_position(camera_x, camera_y)
    gamemap_2.set_position(-camera_x, camera_y)

    loop = True
    while loop:
        caught_events = pygame.event.get()
        for event in caught_events:
            if event.type == pygame.QUIT:
                loop = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                camera_drag = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                camera_drag_x = camera_x - mouse_x
                camera_drag_y = camera_y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                camera_drag = False
            elif event.type == pygame.MOUSEMOTION:
                if camera_drag:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    camera_x = mouse_x + camera_drag_x
                    camera_y = mouse_y + camera_drag_y

                    gamemap_1.set_position(camera_x, camera_y)
                    gamemap_2.set_position(-camera_x, camera_y)

        upd_rects = []
        for canv in canvas_list:
            canv.handle_event(caught_events)
            upd_rects += canv.draw(display)
        pygame.display.update(upd_rects)
        clock.tick(60)


if __name__ == "__main__":
    pygame.display.init()
    main()
    pygame.quit()