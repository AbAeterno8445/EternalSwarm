import pygame
from class_gameSystem import GameSystem


def main():
    display = pygame.display.set_mode((800, 600))
    sys = GameSystem(display)
    sys.loop()


if __name__ == '__main__':
    pygame.display.init()
    pygame.font.init()
    main()
    pygame.quit()