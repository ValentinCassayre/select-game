# -*- coding: utf-8 -*-

"""
Main program file
Coordinates actions
"""

from os import system

from copy import copy

try:
    import pygame
except ModuleNotFoundError:
    print("- Missing Pygame module, try pip install Pygame")
    system("pause")
    exit()

import assets.consts as c
from assets.events import Events
from assets.display import Display
from assets.menu import Menu
from assets.board import Board
from assets.textures import Textures
from assets.game import Game, Time


def main():
    # pygame initialization
    pygame.init()

    # importing the classes
    events = Events()
    display = Display()
    menu = Menu()
    sample_board = Board()
    textures = Textures()  # create all the textures

    time = Time()

    # variables
    # booleans
    update_menu = True

    events.main_loop = True

    game = None

    # creating the board for the first time
    textures.save_board(sample_board.create_board(
        textures.colors["tile outline"],
        textures.game["tile 1"],
        textures.game["tile 2"],
        textures.game["tile mask"]))

    # create all menus
    menu.load(textures)

    # loop while game is open
    while events.main_loop:

        # menu
        if events.state.startswith('menu'):

            menu_name = events.state.split(' ')[-1]
            menu.init(menu_name)

            while events.main_loop and events.state.endswith(menu_name):

                menu.update(menu=menu_name, events=events, textures=textures)
                time.tick()

        # game
        elif events.state == "game":

            # clean screen
            display.draw_screen()

            # check if a game is started, if not start one
            if game is None:
                game_board = copy(sample_board)
                game = Game(game_board, time, textures)
                game.start(textures)
            else:
                game.restart()

            # real game main loop
            while events.main_loop and events.state == "game":

                # limit the frame rate
                time.tick()

                # Events related

                # find the events
                events.check(mask_list=game.board.mask_list)

                # send them to game to update it
                game.send_events(events, textures)

                # Display

                update_display = time.check_display_update()

                if update_display:
                    """
                    update everything on the display except the board
                    """
                    # update caption
                    if display.caption != game.caption:
                        display.set_caption(caption=game.caption)
                    display.draw_screen()

                    # update the screen
                    log_text = str((game.tile_pos, game.turn_number))

                    log = textures.font["menu button"].render(log_text, True, textures.colors["button text"])
                    display.draw_surface_screen(log, c.CENTER, False)

                    # update clock
                    game.update_clock()

                    # table on the right
                    display.draw_table(game.last_turn, game.turn, game.process, game.player_clock, textures)

                    if game.log is not None:
                        display.big_log(game.log[1], textures)

                    game.update_board = True

                if game.update_board:
                    """
                    update only the board
                    """
                    # draw the board to erase old position of the insects for the next update
                    display.draw_surface_screen(textures.game["board"], c.MIDDLE)

                    # draw every overlays on the board (ways, last move, setback)
                    if game.board.draw_ways:
                        # create surface if it needs to be updated
                        for category in game.to_draw_board:

                            if len(game.to_draw_board[category]) > 0:

                                game.board.game_draw(category, game.to_draw_board[category], textures)
                                game.to_draw_board[category] = []

                            # draw the surfaces
                            if game.board.to_draw[category] is not None:
                                display.draw_surface_screen(game.board.to_draw[category], c.CENTER, False)

                    # draw the mouse tile pos
                    display.draw_surface_screen(game.board.mouse_interaction_surface, c.CENTER, False)

                    # draw the insects
                    for tile in game.board.tile_state:
                        if game.board.tile_state[tile] is not None:
                            insect = game.board.tile_state[tile]

                            # draw the insect that is dragged near the mouse
                            if insect is game.tile_insect and game.drag:
                                game.moving_insect = insect

                            else:
                                display.draw_surface_screen(textures.dflt[insect.full_name], game.board.position(insect.pos))

                    if game.moving_insect is not None:
                        if game.disp_drag:
                            display.draw_surface_screen(textures.dflt[game.moving_insect.full_name], events.mouse_pos)

                        else:
                            display.draw_surface_screen(textures.dflt[game.moving_insect.full_name], game.board.position(game.moving_insect.pos))
                        game.moving_insect = None

                if update_display or game.update_board:

                    # update
                    pygame.display.flip()

                    update_display, game.update_board = False, False

        else:  # avoid infinite loop
            events.main_loop = False


# everything starts here
if __name__ == '__Select__':
    main()
