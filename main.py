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
    # pygame initialization
    pygame.init()
    disp = PyDisp()
    board = Board()
    board.create_pos_list()

    # variables
    # booleans
    main_loop = True
    game_started = False
    # strings
    state = "menu"
    game_state = "not started"
    turn = "white"

    # insects of the board initial pos
    a1 = Bug((0, 0), "white")

    # loop while game is open
    while main_loop:
        # menu
        if main_loop and state == "menu":
            # initialize the menu
            game_started = False
            # use disp class to draw the menu page
            disp.draw_menu()
            # update the screen
            pygame.display.flip()

            while main_loop and state == "menu":
                # check mouse and keyboard
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main_loop = False
                    elif event.type == pygame.KEYDOWN:
                        # close windows
                        if event.key == pygame.K_ESCAPE:
                            main_loop = False
                        # enter game
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            state = "game"
                # limit the frame rate
                disp.clock.tick(FPS)

        # game
        if main_loop and state == "game":
            # initialize the game
            if not game_started:
                # this does nothing yet
                disp.game_start()
                # draw board
                board.draw_board()
                # need to add draw insects
                # ---here---

                # now the game is started
                game_started = True
                # prepare the next mode which is to choose the insect for the player
                game_state = "choose insect"

            # real game main loop
            while main_loop and state == "game":
                # update
                pygame.display.flip()
                disp.clock.tick(FPS)

                # draw the board to erase old position of the insects
                # in the future probably need to change to a much optimised thing
                board.draw_board()

                # draw the insects
                pos_bug = board.position((0, 0))
                bug1 = Bug(pos_bug, COLOR_HIGHLIGHT)
                board.draw_insect(bug1.pict, pos_bug)

                # get position of the mouse
                x, y = pygame.mouse.get_pos()

                # get all events
                ev = pygame.event.get()
                # check them all one by one
                for event in ev:
                    # click on close tab
                    if event.type == pygame.QUIT:
                        # stop the script
                        main_loop = False
                    # check keyboard
                    elif event.type == pygame.KEYDOWN:
                        # escape button is pressed
                        if event.key == pygame.K_ESCAPE:
                            # interrupt mode (pause)
                            state = "interrupt"

                # check who needs to play
                # the whites
                if turn == "white":
                    # first step
                    if game_state == "choose insect":
                        for tile in board.mask_list:
                            pos_in_mask = x - tile[0].x, y - tile[0].y
                            touching = tile[0].collidepoint(*(x, y)) and tile[1].get_at(pos_in_mask)
                            if touching:
                                board.highlight_hexagon(board.coords(tile[2]), False)
                            else:
                                pass

                    if game_state == "finished":
                        game_state = "choose insect"
                        turn = "black"
                        disp.clock.tick(FPS)

                # the blacks
                if turn == "black":
                    turn = "white"
                    disp.clock.tick(FPS)

        # interrupt
        if main_loop and state == "interrupt":
            """
            Need to add this
            """
            # temporary close
            main_loop = False


# everything starts here
if __name__ == '__main__':
    main()
