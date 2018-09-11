import pygame
import MSGUI as msgui


class GameSystem(object):
    def __init__(self, display):
        self.display = display
        self.clock = pygame.time.Clock()

        self.canvas_list = {
            "materials": msgui.GUICanvas(16, 16, 200, 500),
            "main": msgui.GUICanvas(232, 16, 552, 500)
        }

        self.canvas_list["materials"].set_background_color((110, 110, 0))
        self.canvas_list["main"].set_background_color((110, 0, 110))

        self.spritetest = msgui.AnimSprite("assets/Mount_Basilisk.png", frames=8)
        self.spritetest.setPosition(32, 32)
        self.canvas_list["main"].add_element(self.spritetest)

        self.spritetest_2 = msgui.SimpleSprite("assets/carbcrystal.png")
        self.spritetest_2.setPosition(32, 0)
        self.canvas_list["main"].add_element(self.spritetest_2)

        self.spritetest_3 = msgui.AnimSprite("assets/Mount_Slime.png", frames=4)
        self.spritetest_3.setPosition(32, 0)
        self.canvas_list["main"].add_element(self.spritetest_3)

    def loop(self):
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

            for canvas in self.canvas_list:
                self.canvas_list[canvas].draw(self.display)

            pygame.display.update()

            self.clock.tick(60)