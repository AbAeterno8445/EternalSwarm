import pygame
import MSGUI


class GameSystem(object):
    def __init__(self, display):
        self.display = display
        self.clock = pygame.time.Clock()

        self.canvas_list = []
        self.canvas_materials = MSGUI.GUICanvas(16, 16, 200, 500)
        self.canvas_main = MSGUI.GUICanvas(232, 16, 552, 500)

        self.canvas_list.append(self.canvas_materials)
        self.canvas_list.append(self.canvas_main)

        self.canvas_materials.set_background_color((110, 110, 0))
        self.canvas_materials.set_border(1, (255, 0, 0))
        self.canvas_main.set_background_color((0, 110, 110))

        self.spritetest = MSGUI.AnimSprite("assets/Mount_Basilisk.png", frames=8)
        self.spritetest.set_position(32, 0)
        self.canvas_main.add_element(self.spritetest)

        self.spritetest_2 = MSGUI.SimpleSprite("assets/carbcrystal.png")
        self.spritetest_2.set_position(32, 64)
        self.canvas_main.add_element(self.spritetest_2)

        self.spritetest_3 = MSGUI.AnimSprite("assets/Mount_Slime.png", frames=4)
        self.spritetest_3.set_position(32, 128)
        self.canvas_main.add_element(self.spritetest_3)

        self.labeltest = MSGUI.Label(32, 196, 70, 24, pygame.font.Font(None, 18), "Hello World!")
        self.labeltest.set_font_color((100, 250, 250))
        self.labeltest.set_auto_resize(True, True)
        self.canvas_main.add_element(self.labeltest, widget=True)

    def loop(self):
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                self.canvas_main.handle_event(event)

            self.canvas_main.draw(self.display)
            self.canvas_materials.draw(self.display)
            pygame.display.update()
            self.clock.tick(60)