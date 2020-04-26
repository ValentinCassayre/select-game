"""
Prototype game by Valentin Cassayre
Github : https://github.com/V-def/select-game
"""

import os

try:
    import pygame
except ModuleNotFoundError:
    print("- Missing pygame module, try pip install pygame")
    exit()

missing_file = False
for file in ["consts.py", "display.py", "insects.py", "textures.py"]:
    if not os.path.exists(os.path.join("assets", file)):
        print("- Missing game file from data folder:", file)
        files_exist = True
if missing_file:
    exit()

from assets.consts import *
from assets.display import *
from assets.insects import *
from assets.textures import *


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
    # lists
    insect_list = []
    ways = []
    eat = []
    # int

    # tuples
    last_tile_pos = tuple
    # other
    tile_insect = None

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
                        insect = Bug(insect_data[2], insect_data[1], textures.insect_path)

                    else:
                        print("[!] Error ! Insect type not recognised.")
                        break

                    board.tile(insect_data[2], True)
                    insect_list.append(insect)
                    # importing insect texture
                    textures.save_insect(insect.full_name, insect.pict)

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
                                    #
                                    for n, insect in enumerate(insect_list):

                                        if insect.pos == tile_pos:
                                            tile_insect = insect

                                            # check if insect is owned by the player
                                            if insect.color == turn:

                                                # get all the possible ways_surface of the insect
                                                ways, eat = calc_ways(tile_insect.calc_ways(), insect_list, turn)

                                                for way_cell in ways:
                                                    disp.draw_surface(
                                                        board.ways_surface,
                                                        textures.dflt["tile_way"],
                                                        board.position(way_cell))

                                                for eat_cell in eat:
                                                    disp.draw_surface(
                                                        board.ways_surface,
                                                        textures.dflt["tile_eat"],
                                                        board.position(eat_cell))

                                                update = True
                                                game_state = "choose way"

                                elif game_state == "choose way":

                                    if tile_pos in ways:
                                        tile_insect.pos = tile_pos
                                        update = True
                                        game_state = "next turn"

                                    elif tile_pos in eat:
                                        for insect in insect_list:
                                            if insect.pos == tile_pos:
                                                insect_list.remove(insect)
                                        tile_insect.pos = tile_pos
                                        update = True
                                        game_state = "next turn"

                                    else:
                                        update = True
                                        game_state = "choose insect"

                                    board.reset_surface("ways_surface")

                            else:
                                # mouse on tile but not clicked
                                # check if the tile is a new tile, else no update of the screen
                                if last_tile_pos != tile[3]:
                                    board.reset_surface("mouse_interaction_surface")
                                    disp.draw_surface(
                                        board.mouse_interaction_surface,
                                        textures.dflt["tile_overview"],
                                        disp_pos)

                                    update = True
                            last_tile_pos = tile[3]

                            # prepare for next turn
                            if game_state == "next turn":
                                possible_mov = [0, 0]

                                # check if game is lost
                                for insect in insect_list:
                                    if insect.color == "white":
                                        # if the insect has no ways to go
                                        a, b = calc_ways(tile_insect.calc_ways(), insect_list, turn)
                                        possible_mov[0] = possible_mov[0] + len(a) + len(b)

                                for insect in insect_list:
                                    if insect.color == "black":
                                        # if the insect has no ways to go
                                        a, b = calc_ways(tile_insect.calc_ways(), insect_list, turn)
                                        possible_mov[1] = possible_mov[1] + len(a) + len(b)

                                if possible_mov[0] == 0 or possible_mov[1] == 0:
                                    print("game over")

                                game_state = "choose insect"
                                if turn == "white":
                                    turn = "black"
                                elif turn == "black":
                                    turn = "white"

                if update:
                    # draw the ways_surface
                    disp.draw_surface(disp.screen, board.ways_surface, CENTER, False)
                    # draw the mouse tile pos
                    disp.draw_surface(disp.screen, board.mouse_interaction_surface, CENTER, False)
                    # draw the insects
                    for insect in insect_list:
                        disp.draw_surface(disp.screen, textures.dflt[insect.full_name], board.position(insect.pos))

                    # update
                    pygame.display.flip()
                    disp.clock.tick(FPS)

                    # draw the board to erase old position of the insects for the next update
                    disp.draw_surface(disp.screen, textures.dflt["board"], MIDDLE)

                    # reset
                    update = False

        # interrupt
        if main_loop and state == "interrupt":
            """
            Need to add this
            """
            # temporary close
            main_loop = False


def calc_ways(lists, insect_list, turn):
    ways, eat = lists
    ways2 = []
    eat2 = []
    # remove all ways_surface that are not possible
    for cell in ways:
        if cell in map(lambda ins: ins.pos, insect_list):
            # another insect is on this tile so it cant go
            pass
        else:
            ways2.append(cell)

    # check if he can eat insects around
    for cell in eat:
        for insect in insect_list:
            # another insect is on this tile so it can eat it
            if insect.pos == cell and insect.color != turn:
                eat2.append(cell)
    return ways2, eat2


# everything starts here
if __name__ == '__main__':
    main()
