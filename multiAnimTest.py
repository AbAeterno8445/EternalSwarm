import pygame
from pygame.locals import DOUBLEBUF
import MSGUI
import math


def main():
    display = pygame.display.set_mode((800, 600), DOUBLEBUF)
    pygame.display.set_caption("MSGUI Multiple animated sprites test")
    clock = pygame.time.Clock()

    canvas = MSGUI.GUICanvas(0, 0, 800, 600, (0, 0, 60))

    slime_img = pygame.image.load("assets/Mount_Slime.png")
    for i in range(1000):
        tmp_x = 18 * (i % 44)
        tmp_y = 18 * math.floor(i / 44)
        tmp_sprite = MSGUI.AnimSprite(tmp_x, tmp_y, 16, 16, slime_img, 4, False)
        canvas.add_element(tmp_sprite, widget=True)

    loop = True
    while loop:
        caught_events = pygame.event.get()
        for event in caught_events:
            if event.type == pygame.QUIT:
                loop = False
                break

        canvas.handle_event(caught_events)
        pygame.display.update(canvas.draw(display))

        clock.tick(60)


if __name__ == "__main__":
    pygame.display.init()
    main()
    pygame.quit()