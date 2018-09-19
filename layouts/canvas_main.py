import pygame
import MSGUI


def testfunct():
    print("hey it works")


def create_canvas_main():
    canvas_main = MSGUI.GUICanvas(232, 16, 552, 500)
    canvas_main.backg_widget.set_background((0, 110, 110))

    return canvas_main