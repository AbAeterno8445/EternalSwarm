import pygame
import MSGUI


def testfunct():
    print("hey it works")


def create_canvas_main():
    canvas_main = MSGUI.GUICanvas(232, 16, 552, 500)

    canvas_main.backg_widget.set_background((0, 110, 110))

    spritetest = MSGUI.AnimSprite(32, 32, 80, 40, "assets/Mount_Basilisk.png", frames=8, autosize=False)
    spritetest.set_icon_autoscale(True)
    spritetest.set_border(True)
    canvas_main.add_element(spritetest, widget="spritetest")

    widgtest = MSGUI.Widget(32, 256, 64, 64)
    widgtest.set_background((0, 255, 150))
    canvas_main.add_element(widgtest, widget="widgtest")

    labeltest = MSGUI.Label(32, 196, 212, 64, pygame.font.Font("assets/Dosis.otf", 32), "Hello World!")
    labeltest.set_font_color((255, 0, 0))
    labeltest.set_text_resize(res_hor=True, padding=32)
    labeltest.set_transparent(True)
    labeltest.set_border(True, (255, 0, 0))
    canvas_main.add_element(labeltest, widget="labeltest")

    buttontest = MSGUI.Button(256, 96, 96, 96, pygame.font.Font("assets/Dosis.otf", 18), callback=testfunct)
    buttontest.set_icon_autoscale(True)
    buttontest.set_icon("assets/carbcrystal.png")
    buttontest.set_hovered_color((110, 255, 0, 150))
    buttontest.set_pressed_color((255, 110, 0, 150))
    buttontest.set_border(True)
    canvas_main.add_element(buttontest, widget="buttontest")

    icontest = MSGUI.ImageWidget(256, 32, 16, 16, "assets/carbcrystal.png", True)
    canvas_main.add_element(icontest, widget="icontest")

    return canvas_main