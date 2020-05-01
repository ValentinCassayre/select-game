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

import assets.consts as c
from assets.events import Events
from assets.display import PyDisp, Board
from assets.insects import Bug, Locust, Spider, Beetle, Bee, Ant, Custom
from assets.textures import Textures
from assets.game import Game


def main():
    # pygame initialization
    pygame.init()

    # importing the classes
    events = Events
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

    initial_layout = (Bug, (0, 3), "white"), (Bug, (1, 3), "white"), (Bug, (2, 3), "white"),\
                     (Bug, (3, 0), "white"), (Bug, (3, 1), "white"), (Bug, (3, 2), "white"), (Bug, (3, 3), "white"),\
                     (Locust, (1, 2), "white"), (Locust, (2, 1), "white"),\
                     (Spider, (0, 2), "white"), (Spider, (2, 0), "white"),\
                     (Beetle, (1, 0), "white"), (Beetle, (0, 1), "white"),\
                     (Bee, (1, 1), "white"), (Bee, (2, 2), "white"),\
                     (Ant, (0, 0), "white"),\
                     (Bug, (6, 9), "black"), (Bug, (6, 8), "black"), (Bug, (6, 7), "black"),\
                     (Bug, (9, 6), "black"), (Bug, (8, 6), "black"), (Bug, (7, 6), "black"), (Bug, (6, 6), "black"),\
                     (Locust, (7, 8), "black"), (Locust, (8, 7), "black"),\
                     (Spider, (7, 9), "black"), (Spider, (9, 7), "black"),\
                     (Beetle, (9, 8), "black"), (Beetle, (8, 9), "black"),\
                     (Bee, (8, 8), "black"), (Bee, (7, 7), "black"),\
                     (Ant, (9, 9), "black"),\

    # creating the board for the first time
    textures.save_board(board.create_board(
        textures.colors["COLOR_TILE_OUTLINE"],
        textures.game["tile_1"],
        textures.game["tile_2"],
        textures.game["tile_mask"]))

    game = Game(disp, board, textures)

    # loop while game is open
    while game.loop:
        # menu
        if game.loop and game.state == "menu":

            # initialize the menu
            # use disp class to draw the menu page
            menu_masks, bg_surface, texts_surface = disp.draw_menu(textures)
            button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
            # update the screen
            pygame.display.flip()

            last_touched_mask = None

            while game.loop and game.state == "menu":

                # check events
                event, mask_touching, click = events.check(menu_masks)

                if event in ["leave", "escape"]:
                    game.stop()

                if event in ["space", "enter"]:
                    game.state = "game"

                for touched_mask in mask_touching:

                    if touched_mask[3].startswith("but"):

                        if click:
                            if touched_mask[3] == "but_1":
                                pass
                            elif touched_mask[3] == "but_2":
                                game.state = "game"
                            elif touched_mask[3] == "but_3":
                                pass
                            elif touched_mask[3] == "but_3":
                                pass

                        elif last_touched_mask is not touched_mask[3]:
                            button = disp.draw_surface(button, textures.dflt["button_overlay"], touched_mask[2])
                            update = True
                            last_touched_mask = touched_mask[3]

                if update:

                    disp.draw_surfaces([bg_surface, button, texts_surface])
                    button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
                    pygame.display.flip()
                    update = False

                # limit the frame rate
                disp.clock.tick(c.FPS)

        # game
        if game.loop and game.state == "game":

            disp.draw_screen()
            disp.draw_surface(disp.screen, textures.game["board"], c.CENTER, False)
            update = True

            # initialize the game
            if not game.started:

                # prepare the initial position of the insects
                for insect_data in initial_layout:

                    insect = insect_data[0](insect_data[1], insect_data[2], textures.insect_path)
                    # update tile
                    board.tile(insect.pos, insect)
                    # add the insect to the other
                    game.insects.append(insect)
                    # importing insect texture
                    textures.save_insect(insect.full_name, insect.pict)

            # real game main loop
            while game.loop and game.state == "game":

                # limit the frame rate
                disp.clock.tick(c.FPS)

                # find the event
                event, mask_touching, click = events.check(mask_list=board.mask_list)

                if event == "leave":
                    game.stop()

                if event == "escape":
                    game.state = "interrupt"

                for touched_mask in mask_touching:

                    if touched_mask[3] == "tile":

                        update, tile_pos = board.draw_tile_overview(touched_mask, textures)

                # act after a click
                if click:
                    click = False

                    if game.process == "choose insect":

                        # return the object of the tile insect if the insect can be selected
                        tile_insect = game.select_insect(tile_pos)

                        # check is something has been selected
                        if tile_insect is not None:

                            ways, eat = board.check_tiles(tile_insect)

                            for way_cell in ways:
                                disp.draw_surface(
                                    board.ways_surface,
                                    textures.game["tile_way"],
                                    board.position(way_cell))

                            for eat_cell in eat:
                                disp.draw_surface(
                                    board.ways_surface,
                                    textures.game["tile_eat"],
                                    board.position(eat_cell))

                            update = True
                            game.process = "choose way"

                    elif game.process == "choose way":

                        if tile_pos in ways:
                            board.tile(tile_insect.pos, None)
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

                if update:
                    # draw the ways_surface
                    disp.draw_surface(disp.screen, board.ways_surface, c.CENTER, False)
                    # draw the mouse tile pos
                    disp.draw_surface(disp.screen, board.mouse_interaction_surface, c.CENTER, False)

                    # draw the insects
                    for insect in game.insects:
                        disp.draw_surface(disp.screen, textures.dflt[insect.full_name], board.position(insect.pos))

                    # update
                    pygame.display.flip()
                    disp.clock.tick(c.FPS)

                    # draw the board to erase old position of the insects for the next update
                    disp.draw_surface(disp.screen, textures.game["board"], c.MIDDLE)

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
