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

from assets.display import Display
from assets.textures import Textures
from assets.events import Events
from assets.settings import Settings
from assets.time import Time, Clock
from assets.chat import ChatBox
from assets.menu import Menu
from assets.board import Board
from assets.gamemodes import Offline, Computer, Online, Tutorial


def main():
    # pygame initialization
    pygame.init()

    # importing the classes
    events = Events()
    display = Display()
    menu = Menu()
    sample_board = Board()
    textures = Textures()  # create all the textures
    settings = Settings()

    time = Time()

    # variables
    # booleans

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

                menu.update(menu=menu_name, events=events, settings=settings, textures=textures)
                time.tick()

        # game
        elif events.state == "game":

            # clean screen
            display.draw_screen()

            # check if a game is started, if not start one
            if game is None:
                game_board = copy(sample_board)
                clock = Clock(settings)
                chat = ChatBox()
                if settings.game['mode'] == 'offline':
                    game = Offline(board=game_board, textures=textures, clock=clock, chat=chat, settings=settings)
                elif settings.game['mode'] == 'computer':
                    game = Computer(board=game_board, textures=textures, clock=clock, chat=chat, settings=settings)
                elif settings.game['mode'] == 'online':
                    game = Online(board=game_board, textures=textures, clock=clock, chat=chat, settings=settings)
                elif settings.game['mode'] == 'tutorial':
                    game = Tutorial(board=game_board, textures=textures, clock=clock, chat=chat, settings=settings)
                else:
                    return

                game.start(textures)
            else:
                game.restart()

            # real game main loop
            while events.main_loop and events.state == "game":

                # limit the frame rate
                time.tick()

                # Events related
                game.send_events(events, textures)

                # Display
                game.check_updates(textures)
                game.update_screen(display=display, textures=textures, events=events)

        else:  # avoid infinite loop
            events.main_loop = False


# everything starts here
if __name__ == '__Select__':
    main()
