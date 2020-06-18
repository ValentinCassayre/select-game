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
from assets.game import Game, Time


def main():
    # pygame initialization
    pygame.init()

    # importing the classes
    events = Events()
    disp = Display()
    board = Board()
    textures = Textures()  # create all the textures

    time = Time()

    # variables
    # booleans
    update_menu = True
    update_board = True
    update_disp = True

    main_loop = True
    state = "menu"

    game = None

    # creating the board for the first time
    textures.save_board(board.create_board(
        textures.colors["tile outline"],
        textures.game["tile 1"],
        textures.game["tile 2"],
        textures.game["tile mask"]))

    # loop while game is open
    while main_loop:
        # menu
        if main_loop and state == "menu":

            # initialize the menu
            # use disp class to draw the menu page
            menu_masks, bg_surface, texts_surface = disp.create_main_menu(textures)
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
                            button = disp.draw_surface_screen(textures.dflt["button overlay"],
                                                              touched_mask[2], on_this_surface=button)
                            update_menu = True
                            last_touched_mask = touched_mask[3]

                if update_menu:

                    disp.draw_screen()
                    disp.draw_surfaces([bg_surface, button, texts_surface])
                    button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
                    pygame.display.flip()
                    update_menu = False

                # limit the frame rate
                time.tick()

        # menu 2 // infos
        if main_loop and state == "infos":

            # initialize the menu
            # use disp class to draw the menu page
            menu_masks, bg_surface, texts_surface = disp.create_infos_menu(textures)
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
                            button = disp.draw_surface_screen(textures.dflt["button overlay"],
                                                              touched_mask[2], on_this_surface=button)
                            update_menu = True
                            last_touched_mask = touched_mask[3]

                if update_menu:
                    disp.draw_screen()
                    disp.draw_surfaces([bg_surface, button, texts_surface])
                    button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
                    pygame.display.flip()
                    update_menu = False

                # limit the frame rate
                time.tick()

        # interrupt
        if main_loop and state == "interrupt":

            # initialize the menu
            # use disp class to draw the menu page
            menu_masks, bg_surface, texts_surface = disp.create_interrupt_menu(textures)
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
                            button = disp.draw_surface_screen(textures.dflt["button overlay"],
                                                              touched_mask[2], on_this_surface=button)
                            update_menu = True
                            last_touched_mask = touched_mask[3]

                if update_menu:
                    disp.draw_screen()
                    disp.draw_surfaces([bg_surface, button, texts_surface])
                    button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
                    pygame.display.flip()
                    update_menu = False

                # limit the frame rate
                time.tick()

        # game
        if main_loop and state == "game":

            # clean screen
            disp.draw_screen()

            # check if a game is started, if not start one
            if game is None:
                game = Game(board, textures, time)
                game.start()
            else:
                game.restart()

            # draw board
            disp.draw_surface_screen(textures.game["board"], c.CENTER, False)

            update_board = True

            selected_insect = None
            drag = False

            last_update = time.stopwatch.get_ticks()

            # real game main loop
            while main_loop and state == "game":

                # limit the frame rate
                time.tick()

                # Events related

                # find the events
                events.check(mask_list=board.mask_list)

                if events.key == "leave":
                    main_loop = False

                if events.key == "escape":
                    state = "interrupt"

                # draw overlay
                for touched_mask in events.mask_touching:

                    if touched_mask[3] == "tile":

                        update_board, game.tile_pos = board.draw_tile_overview(touched_mask, textures)

                if not game.ended:

                    if game.process == "next turn":

                        game.process = "choose insect"
                        game.change_turn()

                    # act after a click
                    if events.click:

                        drag = True

                        if game.process == "choose insect":

                            update_board, selected_insect = game.choose_insect(textures)

                    elif drag and not events.mouse_but_down:

                        if game.process == "choose way":

                            update_board, selected_insect = game.choose_way(textures, drag=drag)
                            drag = False

                else:

                    # end game state

                    pass

                # Display

                if last_update/100 != time.stopwatch.get_ticks()/100:
                    last_update = time.stopwatch.get_ticks()
                    update_disp = True

                if update_disp:
                    """
                    update everything on the display except the board
                    """
                    disp.draw_screen()

                    # update the screen
                    log_text = str((game.tile_pos, game.turn_number))

                    log = textures.font["menu button"].render(log_text, True, textures.colors["button text"])
                    disp.draw_surface_screen(log, c.CENTER, False)

                    # update clock
                    game.update_clock()

                    # table on the right
                    disp.draw_table(game.last_turn, game.turn, game.process, game.player_clock, textures)

                    if game.log is not None:
                        disp.big_log(game.log[1], textures)

                    update_board = True

                    time.tick()

                if update_board:
                    """
                    update only the board
                    """

                    # draw the board to erase old position of the insects for the next update
                    disp.draw_surface_screen(textures.game["board"], c.MIDDLE)

                    # draw the ways_surface
                    disp.draw_surface_screen(board.ways_surface, c.CENTER, False)

                    # draw last move
                    disp.draw_surface_screen(board.last_move_surface, c.CENTER, False)

                    # draw setback
                    if game.setback is not None:
                        disp.draw_surface_screen(textures.game['tile setback'], board.position(game.setback.pos), True)

                    # draw the mouse tile pos
                    disp.draw_surface_screen(board.mouse_interaction_surface, c.CENTER, False)

                    # draw the insects
                    for tile in board.tile_state:
                        if board.tile_state[tile] is not None:
                            insect = board.tile_state[tile]

                            if insect == selected_insect and drag:
                                disp.draw_surface_screen(textures.dflt[insect.full_name], events.mouse_pos)
                            else:
                                disp.draw_surface_screen(textures.dflt[insect.full_name], board.position(insect.pos))

                    time.tick()

                if update_disp or update_board:

                    # update
                    pygame.display.flip()
                    time.tick()

                    update_disp, update_board = False, False


# everything starts here
if __name__ == '__Select__':
    main()
