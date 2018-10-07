import pygame
from pygame.locals import DOUBLEBUF
from playerdata import PlayerData
import layouts


def main():
    # Init display & clock
    display = pygame.display.set_mode((800, 600), DOUBLEBUF)
    pygame.display.set_caption("Eternal Swarm")
    display_icon = pygame.transform.scale(pygame.image.load("assets/materials/sapphire.png"), (64, 64))
    pygame.display.set_icon(display_icon)
    clock = pygame.time.Clock()

    # Player data holder
    player_data = PlayerData("Player")

    # Init screens
    screen_main = layouts.ScreenMain(display, player_data)
    screen_levelinfo = layouts.ScreenLevelInfo(display)
    screen_game = layouts.ScreenGame(display, player_data)

    current_screen = "main"
    screens = {
        "main": screen_main,
        "levelinfo": screen_levelinfo,
        "game": screen_game
    }

    frame = 0
    loop = True
    while loop:
        caught_events = pygame.event.get()
        for event in caught_events:
            if event.type == pygame.QUIT:
                loop = False
                break

        frame = (frame + 1) % 60

        if frame % 5 == 0:
            player_data.ccps_tick(12)

        cur_screen = screens[current_screen]
        upd_rects = cur_screen.update(caught_events)

        screen_switch = cur_screen.get_switch_screen()
        if screen_switch:
            current_screen = screen_switch
            screens[current_screen].init_screen(cur_screen)

        pygame.display.update(upd_rects)
        clock.tick(60)


if __name__ == '__main__':
    pygame.display.init()
    pygame.font.init()
    main()
    pygame.quit()