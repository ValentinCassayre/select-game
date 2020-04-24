"""
Prototype game by Valentin Cassayre
Github : https://github.com/V-def/select-game
"""

import pygame
import math
from consts import *
from display import *
from textures import *
from insects import *
from texture_pack import *


def main():
    # pygame initialization
    pygame.init()
    disp = PyDisp()
    board = Board()
    textures = Textures()  # create all the textures

    # variables
    # booleans
    main_loop = True
    game_started = False
    update = True
    # strings
    state = "menu"
    game_state = "not started"
    turn = "white"

    insect_list = []

    for n, insect in enumerate(INSECT_LIST):
        ins_pos = INITIAL_POSITION[n]
        if insect.startswith("bug"):
            insect = Bug(ins_pos, "white")
        elif insect.startswith("aaa"):
            pass
        # add all the insects types here
        else:
            print("Error with the insect list ! Insects needs to start with their role name.")
        board.tile(ins_pos, True)
        insect_list.append(insect)

    # creating the board for the first time
    textures.save_board(board.create_board(
        textures.colors["COLOR_TILE_OUTLINE"], textures.dflt["tile_1"], textures.dflt["tile_1"], textures.dflt["tile_mask"]))

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

            disp.draw_surface(disp.screen, textures.dflt["board"], CENTER, False)

            # initialize the game
            if not game_started:
                # now the game is started
                game_started = True
                # prepare the next mode which is to choose the insect for the player
                game_state = "choose insect"

            # real game main loop
            while main_loop and state == "game":

                # get the position of the mouse
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
                    # check mouse
                    for tile in board.mask_list:
                        # tile[n] : 0 rect 1 mask 2 disp pos 3 board pos
                        pos_in_mask = x - tile[0].x, y - tile[0].y
                        touching = tile[0].collidepoint(*(x, y)) and tile[1].get_at(pos_in_mask)

                        if touching:
                            disp_pos = tile[2]
                            tile_pos = tile[3]
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # tile clicked
                                # check what is on this tile and put it in tile_obj
                                tile_obj = ""
                                for insect in insect_list:
                                    if insect.pos == tile_pos:
                                        tile_obj = insect

                                # do something with it ?
                                if tile_obj == "":
                                    # tile is free
                                    disp.draw_surface(disp.screen, textures.dflt["tile_select"], disp_pos)

                                elif game_state == "choose insect":
                                    if tile_obj.color == turn:

                                        # there is an insect owned by the player
                                        # -> draw ways
                                        # game_state = "choose way"
                                        pass

                                elif game_state == "choose way":
                                    # if tile is a way
                                        # tile_obj new pos = tile clicked
                                            # if eat
                                                # del insect eaten

                                        # prepare next turn
                                        # game_state == "choose insect"
                                        # if turn == "white":
                                            # turn = "black"
                                        # elif turn == "black":
                                            # turn = "white"
                                    pass
                            else:
                                # mouse on tile but not clicked
                                disp.draw_surface(disp.screen, textures.dflt["tile_overview"], disp_pos)
                            update = True

                if update:
                    # draw the insects
                    for insect in insect_list:
                        rect = textures.dflt["ins_bug"].get_rect()
                        rect.center = board.position(insect.pos)
                        disp.screen.blit(textures.dflt["ins_bug"], rect)

                    # update
                    pygame.display.flip()
                    disp.clock.tick(FPS)

                    # draw the board to erase old position of the insects for the next update
                    disp.draw_surface(disp.screen, textures.dflt["board"], MIDDLE)

                    # reset
                    update = False

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
