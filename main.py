import pygame
from pygame.locals import DOUBLEBUF
import MSGUI


def testfunct():
    print("hey it works")


def main():
    # Init display
    display = pygame.display.set_mode((800, 600), DOUBLEBUF)
    pygame.display.set_caption("Eternal Swarm")

    clock = pygame.time.Clock()

    canvas_materials = MSGUI.GUICanvas(16, 16, 200, 500)
    canvas_main = MSGUI.GUICanvas(232, 16, 552, 500)
    canvas_list = (canvas_materials, canvas_main)

    canvas_materials.backg_widget.set_background((110, 110, 0))
    canvas_materials.backg_widget.set_border(1, (255, 0, 0))
    canvas_main.backg_widget.set_background((0, 110, 110))

    spritetest = MSGUI.AnimSprite(32, 32, 80, 40, "assets/Mount_Basilisk.png", frames=8, autosize=True)
    spritetest.set_border(True)
    canvas_main.add_element(spritetest, widget=True)

    widgtest = MSGUI.Widget(32, 256, 64, 64)
    widgtest.set_background((0, 255, 150))
    canvas_main.add_element(widgtest, widget=True)

    labeltest = MSGUI.Label(32, 196, 212, 64, pygame.font.Font("assets/Dosis.otf", 32), "Hello World!")
    labeltest.set_font_color((255, 0, 0))
    labeltest.set_text_resize(res_hor=True, padding=32)
    labeltest.set_transparent(True)
    labeltest.set_border(True, (255, 0, 0))
    canvas_main.add_element(labeltest, widget=True)

    buttontest = MSGUI.Button(256, 96, 96, 96, pygame.font.Font("assets/Dosis.otf", 18), callback=testfunct)
    buttontest.set_icon("assets/carbcrystal.png")
    buttontest.set_hovered_color((110, 255, 0, 150))
    buttontest.set_pressed_color((255, 110, 0, 150))
    buttontest.set_border(True)
    canvas_main.add_element(buttontest, widget=True)

    icontest = MSGUI.Imagebox(256, 32, 16, 16, "assets/carbcrystal.png", True)
    canvas_main.add_element(icontest, widget=True)

    loop = True
    ii = 0
    while loop:
        ii += 100
        caught_events = pygame.event.get()
        for event in caught_events:
            if event.type == pygame.QUIT:
                loop = False
                break

        labeltest.set_text(str(ii))
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