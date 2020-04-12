"""
Prototype game by Valentin Cassayre
Git : https://github.com/V-def/select-game
"""

import pygame
import math
from consts import *
from display import *
from board import *
from insects import *


def main():
    pygame.init()

    disp = PyDisp()
    main_condition = True

    pygame.display.set_caption(GAME_NAME)

    # loop while game is open
    while main_condition:

        # update screen for background
        pygame.display.flip()

        # player close windows
        for event in pygame.event.get():
            # event closing
            if event.type == pygame.QUIT:
                main_condition = False
                pygame.quit()
                print("Closing select!")


# everything starts here
if __name__ == '__main__':
    main()
