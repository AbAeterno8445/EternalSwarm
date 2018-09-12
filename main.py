import pygame
from pygame.locals import DOUBLEBUF
import MSGUI


def main():
    # Init display
    display = pygame.display.set_mode((800, 600), DOUBLEBUF)
    pygame.display.set_caption("Eternal Swarm")
    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN])

    clock = pygame.time.Clock()

    canvas_list = []
    canvas_materials = MSGUI.GUICanvas(16, 16, 200, 500)
    canvas_main = MSGUI.GUICanvas(232, 16, 552, 500)

    canvas_list.append(canvas_materials)
    canvas_list.append(canvas_main)

    canvas_materials.set_background_color((110, 110, 0))
    canvas_materials.set_border(1, (255, 0, 0))
    canvas_main.set_background_color((0, 110, 110))

    spritetest = MSGUI.AnimSprite("assets/Mount_Basilisk.png", frames=8)
    spritetest.set_position(32, 96)
    canvas_main.add_element(spritetest)

    spritetest_2 = MSGUI.SimpleSprite("assets/carbcrystal.png")
    spritetest_2.set_position(32, 32)
    canvas_main.add_element(spritetest_2)

    labeltest = MSGUI.Label(32, 196, 70, 24, pygame.font.Font(None, 18), "Hello World!")
    labeltest.set_font_color((100, 250, 250))
    labeltest.set_auto_resize(True, True)
    labeltest.set_padding(16)
    labeltest.set_background((0, 0, 0), True)
    labeltest.set_border(True, (255, 0, 0))
    labeltest.set_hovered(True, (0, 110, 0))
    canvas_main.add_element(labeltest, widget=True)

    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            for canvas in canvas_list:
                canvas.handle_event(event)

        for canvas in canvas_list:
            canvas.draw(display)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    pygame.display.init()
    pygame.font.init()
    main()
    pygame.quit()