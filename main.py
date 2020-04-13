"""
Prototype game by Valentin Cassayre
Git : https://github.com/V-def/select-game
"""

import pygame
import math
from consts import *
from display import *
from insects import *


def main():
    # Pygame initialization
    pygame.init()
    disp = PyDisp()
    board = Board()

    # Windows first settings
    pygame.display.set_caption(GAME_NAME)

    # Variables
    main_loop = True
    game_started = False
    state = "menu"
    turn = "white"

    disp.draw_screen()

    # insects of the board initial pos
    a1 = Bug((0, 0), "white")

    # loop while game is open
    while main_loop:

        if main_loop and state == "menu":

            game_started = False
            disp.draw_menu()

            pygame.display.flip()

            while main_loop and state == "menu":

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main_loop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            main_loop = False
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            state = "game"
                disp.clock.tick(FPS)

        if main_loop and state == "game":
            # Start the game
            if not game_started:
                disp.game_start()
                board.draw_board()
                # need to add draw insects

                game_started = True

            while main_loop and state == "game":
                # draw the board
                board.draw_board()
                # draw the insects
                a1.highlight_ways()
                pygame.display.flip()

                disp.clock.tick(FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main_loop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            state = "interrupt"

                if turn == "white":

                    turn = "black"
                    disp.clock.tick(FPS)
                elif turn == "black":
                    turn = "white"
                    disp.clock.tick(FPS)
                board.draw_board()

            if main_loop and state == "interrupt":
                """
                Need to add this
                """
                main_loop = False


# everything starts here
if __name__ == '__main__':
    main()
