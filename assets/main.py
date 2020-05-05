"""
Main program file
Coordinates actions
"""

from os import system
from webbrowser import open as open_url

try:
    import pygame
except ModuleNotFoundError:
    print("- Missing Pygame module, try pip install Pygame")
    system("pause")
    exit()

import assets.consts as c
from assets.events import Events
from assets.display import Display, Board
from assets.textures import Textures
from assets.game import Game, Tutorial
from assets.initial_layout import InitialLayout


def main():
    # pygame initialization
    pygame.init()

    # importing the classes
    events = Events
    disp = Display()
    board = Board()
    textures = Textures()  # create all the textures
    game = Game(board)
    tutorial = Tutorial(board)

    # variables
    # booleans
    update = True

    # creating the board for the first time
    textures.save_board(board.create_board(
        textures.colors["tile_outline"],
        textures.game["tile_1"],
        textures.game["tile_2"],
        textures.game["tile_mask"]))

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
                                tutorial.start()
                            elif touched_mask[3] == "but_2":
                                game.state = "game"
                            elif touched_mask[3] == "but_3":
                                pass
                            elif touched_mask[3] == "but_4":
                                pass
                            elif touched_mask[3] == "but_5":
                                open_url('http://valentin.cassayre.me/select')
                            elif touched_mask[3] == "but_6":
                                open_url('https://github.com/V-def/select-game')

                        elif last_touched_mask is not touched_mask[3]:
                            button = disp.draw_surface(textures.dflt["button_overlay"],
                                                       touched_mask[2], on_this_surface=button)
                            update = True
                            last_touched_mask = touched_mask[3]

                if update:

                    disp.draw_screen()
                    disp.draw_surfaces([bg_surface, button, texts_surface])
                    button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
                    pygame.display.flip()
                    update = False

                # limit the frame rate
                disp.clock.tick(c.FPS)

        # game
        if game.loop and game.state == "game" or game.state == "tutorial":

            disp.draw_screen()
            disp.draw_surface(textures.game["board"], c.CENTER, False)
            update = True

            # initialize the game
            if not game.started:

                # prepare the initial position of the insects
                for insect_data in InitialLayout.custom():

                    insect = insect_data[0](insect_data[1], insect_data[2], textures.insect_path)
                    # update tile
                    board.tile(insect.pos, insect)
                    # add the insect to the other
                    game.insects.append(insect)
                    # importing insect texture
                    textures.save_insect(insect.full_name, insect.pict)

                game.update_ways()

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

                        update, game.tile_pos = board.draw_tile_overview(touched_mask, textures)

                # act after a click
                if click:

                    if game.process == "choose insect":

                        update = game.choose_insect(board, textures)

                    elif game.process == "choose way":

                        update = game.choose_way(board)

                if update:
                    # update the screen
                    log_text = str(game.setback)
                    log = textures.font["menu button"].render(log_text, True, textures.colors["button_text"])
                    disp.draw_surface(log, c.CENTER, False)

                    # draw the ways_surface
                    disp.draw_surface(board.ways_surface, c.CENTER, False)
                    # draw the mouse tile pos
                    disp.draw_surface(board.mouse_interaction_surface, c.CENTER, False)

                    # draw setback
                    if game.setback is not None:
                        disp.draw_surface(textures.game['tile_setback'], board.position(game.setback.pos), True)

                    # draw the insects
                    for insect in game.insects:
                        disp.draw_surface(textures.dflt[insect.full_name], board.position(insect.pos))

                    # update
                    pygame.display.flip()
                    disp.clock.tick(c.FPS)

                    disp.draw_screen()

                    # draw the board to erase old position of the insects for the next update
                    disp.draw_surface(textures.game["board"], c.MIDDLE)

                    # reset
                    update = False

        # interrupt
        if game.loop and game.state == "interrupt":
            """
            Need to add this (pause)
            """
            # temporary close
            game.stop()


# everything starts here
if __name__ == '__Select__':
    main()
