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

                for event in pygame.event.get():

                    # normal closing
                    if event.type == pygame.QUIT:
                        main_loop = False

                    # check keyboard and mouse
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

                # prepare the initial position of the insects
                insect_list = []

                for n, insect_data in enumerate(INSECT_LIST):

                    # insect data : 0 type 1 color 2 initial pos

                    if insect_data[0] == "bug":
                        insect = Bug(insect_data[2], insect_data[1])

                    else:
                        print("[!] Error ! Insect type not recognised.")
                        break

                    board.tile(insect_data[2], True)
                    insect_list.append(insect)

                # now the game is started
                game_started = True

                # prepare the next mode which is to choose the insect for the player
                game_state = "choose insect"

                last_tile_pos = None

            # real game main loop
            while main_loop and state == "game":

                # limit the frame rate
                disp.clock.tick(FPS)

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

                                if game_state == "choose insect":

                                    # check any insect is on this tile
                                    # if tile_pos in map(lambda ins: ins.pos, insect_list):
                                    for insect_number, insect in enumerate(insect_list):

                                        if insect.pos == tile_pos:
                                            tile_insect = insect

                                            # check if insect is owned by the player
                                            if insect.color == turn:

                                                # get all the possible ways of the insect
                                                ways, eat = tile_insect.calc_ways()
                                                ways2, eat2 = [], []

                                                # remove all ways that are not possible
                                                # an insect from the same team is on the cell
                                                for cell in ways:
                                                    if board.tile_state[cell] is False:
                                                        ways2.append(cell)

                                                # there is nobody to eat there
                                                for cell in eat:
                                                    if board.tile_state[cell] is True:
                                                        eat2.append(cell)

                                                for way_cell in ways2:
                                                    disp.draw_surface(disp.screen, textures.dflt["tile_way"],
                                                                      board.position(way_cell))

                                                for eat_cell in eat2:
                                                    disp.draw_surface(disp.screen, textures.dflt["tile_eat"],
                                                                      board.position(eat_cell))

                                                update = True
                                                game_state = "choose way"

                                elif game_state == "choose way":

                                    if tile_pos in ways2:
                                        update = True

                                    elif tile_pos in eat2:
                                        print("miam")
                                        insect_list[insect_number].pos(tile_pos)
                                        update = True

                                    game_state = "choose insect"
                                    if turn == "white":
                                        turn = "black"
                                    elif turn == "black":
                                        turn = "white"

                            else:
                                # mouse on tile but not clicked
                                # check if the tile is a new tile, else no update of the screen
                                if last_tile_pos != tile[3]:
                                    disp.draw_surface(disp.screen, textures.dflt["tile_overview"], disp_pos)
                                    update = True
                            last_tile_pos = tile[3]

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
                    print(game_state, turn)

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
