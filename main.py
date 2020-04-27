"""
Prototype game by Valentin Cassayre
Github : https://github.com/V-def/select-game
"""

import os

try:
    import pygame
except ModuleNotFoundError:
    print("- Missing pygame module, try pip install pygame")
    os.system("pause")
    exit()

from assets.consts import *
from assets.display import PyDisp, Board
from assets.insects import *
from assets.textures import Textures
from assets.game import Game


def main():
    # pygame initialization
    pygame.init()

    # importing the classes
    disp = PyDisp()
    board = Board()
    textures = Textures()  # create all the textures

    # variables
    # booleans
    update = True
    click = False
    # lists
    ways = []
    eat = []

    # other
    insect = None
    tile_insect = None
    tile_pos = None

    # creating the board for the first time
    textures.save_board(board.create_board(
        textures.colors["COLOR_TILE_OUTLINE"],
        textures.dflt["tile_1"],
        textures.dflt["tile_1"],
        textures.dflt["tile_mask"]))

    game = Game()

    # loop while game is open
    while game.loop:
        # menu
        if game.loop and game.state == "menu":
            # initialize the menu
            # use disp class to draw the menu page
            disp.draw_menu()
            # update the screen
            pygame.display.flip()

            while game.loop and game.state == "menu":

                for event in pygame.event.get():

                    # normal closing
                    if event.type == pygame.QUIT:
                        game.stop()

                    # check keyboard and mouse
                    elif event.type == pygame.KEYDOWN:

                        # close windows
                        if event.key == pygame.K_ESCAPE:
                            game.stop()

                        # enter game
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            game.state = "game"

                # limit the frame rate
                disp.clock.tick(FPS)

        # game
        if game.loop and game.state == "game":

            disp.draw_surface(disp.screen, textures.dflt["board"], CENTER, False)

            # initialize the game
            if not game.started:

                # prepare the initial position of the insects
                for n, insect_data in enumerate(INSECT_LIST):

                    # insect data : 0 type 1 color 2 initial pos

                    if insect_data[0] == "bug":
                        insect = Bug(insect_data[2], insect_data[1], textures.insect_path)

                    elif insect_data[0] == "locust":
                        insect = Locust(insect_data[2], insect_data[1], textures.insect_path)

                    else:
                        print("- Error : Insect type not recognised.")
                        game.stop()

                    # update tile
                    board.tile(insect.pos, insect)
                    # add the insect to the other
                    game.insects.append(insect)
                    # importing insect texture
                    textures.save_insect(insect.full_name, insect.pict)

                # prepare the next mode which is to choose the insect for the player
                game.process = "choose insect"
                game.started = True

            # real game main loop
            while game.loop and game.state == "game":

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
                        game.stop()

                    # check keyboard
                    elif event.type == pygame.KEYDOWN:
                        # escape button is pressed
                        if event.key == pygame.K_ESCAPE:
                            # interrupt mode (pause)
                            game.state = "interrupt"

                    # check mouse
                    for tile in board.mask_list:
                        # tile[n] : 0 rect 1 mask 2 disp pos 3 board pos
                        pos_in_mask = x - tile[0].x, y - tile[0].y
                        touching = tile[0].collidepoint(*(x, y)) and tile[1].get_at(pos_in_mask)

                        if touching:
                            disp_pos = tile[2]
                            tile_pos = tile[3]

                            # check if the tile is a new tile, else no update of the screen
                            if board.last_tile != tile[3]:
                                board.reset_surface("mouse_interaction_surface")
                                disp.draw_surface(
                                    board.mouse_interaction_surface,
                                    textures.dflt["tile_overview"],
                                    disp_pos)

                                update = True
                            board.last_tile = tile[3]

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # tile clicked
                                click = True

                # act after a click
                if click:
                    click = False

                    if game.process == "choose insect":

                        # check any insect is on this tile
                        #
                        for n, insect in enumerate(game.insects):

                            if insect.pos == tile_pos:
                                tile_insect = insect

                                # check if insect is owned by the player
                                if insect.color == game.turn:

                                    # get all the possible tiles where the insect can go
                                    # ways

                                    ways, eat = board.check_tiles(tile_insect)

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
                                    game.process = "choose way"

                    elif game.process == "choose way":

                        if tile_pos in ways:
                            tile_insect.pos = tile_pos
                            board.tile(tile_insect.pos, tile_insect)
                            update = True
                            game.process = "next turn"

                        elif tile_pos in eat:
                            for insect in game.insects:
                                if insect.pos == tile_pos:
                                    game.insects.remove(insect)

                            # update tile before
                            board.tile(tile_insect.pos, None)
                            # move insect
                            tile_insect.pos = tile_pos
                            # update tile after
                            board.tile(tile_insect.pos, tile_insect)
                            update = True
                            game.process = "next turn"

                        else:
                            update = True
                            game.process = "choose insect"

                        board.reset_surface("ways_surface")

                # prepare for next turn
                if game.process == "next turn":

                    # check if game is lost
                    # removed it because it was not well done

                    game.process = "choose insect"
                    game.change_turn()

                if update:
                    # draw the ways_surface
                    disp.draw_surface(disp.screen, board.ways_surface, CENTER, False)
                    # draw the mouse tile pos
                    disp.draw_surface(disp.screen, board.mouse_interaction_surface, CENTER, False)

                    # draw the insects
                    for insect in game.insects:
                        disp.draw_surface(disp.screen, textures.dflt[insect.full_name], board.position(insect.pos))

                    # update
                    pygame.display.flip()
                    disp.clock.tick(FPS)

                    # draw the board to erase old position of the insects for the next update
                    disp.draw_surface(disp.screen, textures.dflt["board"], MIDDLE)

                    # reset
                    update = False

        # interrupt
        if game.loop and game.state == "interrupt":
            """
            Need to add this (pause)
            """
            # temporary close
            game.stop()


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
