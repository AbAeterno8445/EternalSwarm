import pygame
from gameSystem import GameSystem


def main():
    display = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Eternal Swarm")
    sys = GameSystem(display)
    sys.loop()


if __name__ == '__main__':
    pygame.display.init()
    pygame.font.init()
    main()
    pygame.quit()