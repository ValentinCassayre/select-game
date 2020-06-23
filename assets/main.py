"""
Main program file
Coordinates actions
"""

from os import system
from webbrowser import open as open_url
from copy import copy

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
from assets.game import Game, Time


def main():
    # pygame initialization
    pygame.init()

    # importing the classes
    events = Events()
    display = Display()
    sample_board = Board()
    textures = Textures()  # create all the textures

    time = Time()

    # variables
    # booleans
    update_menu = True

    main_loop = True
    state = "menu"

    game = None

    # creating the board for the first time
    textures.save_board(sample_board.create_board(
        textures.colors["tile outline"],
        textures.game["tile 1"],
        textures.game["tile 2"],
        textures.game["tile mask"]))

    # loop while game is open
    while main_loop:

        # update default window name
        display.set_caption()

        # menu
        if main_loop and state == "menu":

            # initialize the menu
            # use disp class to draw the menu page
            menu_masks, bg_surface, texts_surface = display.create_main_menu(textures)
            button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
            # update the screen
            pygame.display.flip()

            last_touched_mask = None

            while main_loop and state == "menu":

                # check events
                events.check(mask_list=menu_masks)

                if events.key in ["leave", "escape"]:
                    main_loop = False

                if events.key in ["space", "enter"]:
                    state = "game"

                for touched_mask in events.mask_touching:

                    if touched_mask[3].startswith("but"):

                        if events.click:
                            if touched_mask[3] == "but_1":
                                # tutorial here
                                pass
                            elif touched_mask[3] == "but_2":
                                state = "game"
                            elif touched_mask[3] == "but_3":
                                pass
                            elif touched_mask[3] == "but_4":
                                state = "infos"
                            break

                        elif last_touched_mask is not touched_mask[3]:
                            button = display.draw_surface_screen(textures.dflt["button overlay"],
                                                                 touched_mask[2], on_this_surface=button)
                            update_menu = True
                            last_touched_mask = touched_mask[3]

                if update_menu:

                    display.draw_screen()
                    display.draw_surfaces([bg_surface, button, texts_surface])
                    button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
                    pygame.display.flip()
                    update_menu = False

                # limit the frame rate
                time.tick()

        # menu 2 // infos
        if main_loop and state == "infos":

            # initialize the menu
            # use disp class to draw the menu page
            menu_masks, bg_surface, texts_surface = display.create_infos_menu(textures)
            button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
            # update the screen
            update_menu = True

            last_touched_mask = None

            while main_loop and state == "infos":

                # check events
                events.check(menu_masks)

                if events.key is "leave":
                    main_loop = False

                if events.key is "escape":
                    state = "menu"

                if events.key in ["space", "enter"]:
                    open_url('https://github.com/V-def/select-game')

                for touched_mask in events.mask_touching:

                    if touched_mask[3].startswith("but"):

                        if events.click:
                            if touched_mask[3] == "but_1":
                                open_url('https://github.com/V-def/select-game')
                            elif touched_mask[3] == "but_2":
                                open_url('http://valentin.cassayre.me/select')
                            elif touched_mask[3] == "but_3":
                                state = "menu"
                            elif touched_mask[3] == "but_4":
                                main_loop = False
                            break

                        elif last_touched_mask is not touched_mask[3]:
                            button = display.draw_surface_screen(textures.dflt["button overlay"],
                                                                 touched_mask[2], on_this_surface=button)
                            update_menu = True
                            last_touched_mask = touched_mask[3]

                if update_menu:
                    display.draw_screen()
                    display.draw_surfaces([bg_surface, button, texts_surface])
                    button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
                    pygame.display.flip()
                    update_menu = False

                # limit the frame rate
                time.tick()

        # interrupt
        if main_loop and state == "interrupt":

            # initialize the menu
            # use disp class to draw the menu page
            menu_masks, bg_surface, texts_surface = display.create_interrupt_menu(textures)
            button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
            # update the screen
            update_menu = True

            last_touched_mask = None

            while main_loop and state == "interrupt":

                # check events
                events.check(menu_masks)

                if events.key in ["leave", "escape"]:
                    main_loop = False

                if events.key in ["space", "enter"]:
                    state = "game"

                for touched_mask in events.mask_touching:

                    if touched_mask[3].startswith("but"):

                        if events.click:
                            if touched_mask[3] == "but_1":
                                # save
                                pass
                            elif touched_mask[3] == "but_2":
                                # resume
                                state = "game"
                            elif touched_mask[3] == "but_3":
                                # quit
                                main_loop = False
                            elif touched_mask[3] == "but_4":
                                # github
                                open_url('https://github.com/V-def/select-game')
                            break

                        elif last_touched_mask is not touched_mask[3]:
                            button = display.draw_surface_screen(textures.dflt["button overlay"],
                                                                 touched_mask[2], on_this_surface=button)
                            update_menu = True
                            last_touched_mask = touched_mask[3]

                if update_menu:
                    display.draw_screen()
                    display.draw_surfaces([bg_surface, button, texts_surface])
                    button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
                    pygame.display.flip()
                    update_menu = False

                # limit the frame rate
                time.tick()

        # game
        if main_loop and state == "game":

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
            while main_loop and state == "game":

                # limit the frame rate
                time.tick()

                # Events related

                # find the events
                events.check(mask_list=game.board.mask_list)

                # send them to game to update it
                main_loop, state = game.send_events(events, textures)

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


# everything starts here
if __name__ == '__Select__':
    main()
