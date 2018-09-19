import pygame
from pygame.locals import DOUBLEBUF
import MSGUI
from TileTest.gameMap import GameMap


def main():
    display = pygame.display.set_mode((800, 600), DOUBLEBUF)
    pygame.display.set_caption("MSGUI Tiling test")
    clock = pygame.time.Clock()

    canvas_main = MSGUI.GUICanvas(0, 0, 800, 600, (0, 50, 50))

    gamemap = GameMap(0, 0, 8, 8)
    canvas_main.add_element(gamemap)

    camera_x = display.get_width() / 2 - gamemap.width * 24
    camera_y = display.get_height() / 2 - gamemap.height * 24
    camera_drag = False
    camera_drag_x = 0
    camera_drag_y = 0

    gamemap.set_position(camera_x, camera_y)

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

                    gamemap.set_position(camera_x, camera_y)

        canvas_main.handle_event(caught_events)
        pygame.display.update(canvas_main.draw(display))
        clock.tick(60)


if __name__ == "__main__":
    pygame.display.init()
    main()
    pygame.quit()