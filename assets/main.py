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
    events = Events()
    disp = Display()
    board = Board()
    textures = Textures()  # create all the textures
    game = Game(board)
    tutorial = Tutorial(board)

    # variables
    # booleans
    update_menu = True
    update_board = True
    update_disp = True

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
            menu_masks, bg_surface, texts_surface = disp.create_main_menu(textures)
            button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
            # update the screen
            pygame.display.flip()

            last_touched_mask = None

            while game.loop and game.state == "menu":

                # check events
                event, mask_touching, click = events.check(mask_list=menu_masks)

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
                                game.state = "infos"

                        elif last_touched_mask is not touched_mask[3]:
                            button = disp.draw_surface(textures.dflt["button_overlay"],
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
                game.clock.tick(c.FPS)

        # interrupt
        if game.loop and game.state == "infos":

            # initialize the menu
            # use disp class to draw the menu page
            menu_masks, bg_surface, texts_surface = disp.create_infos_menu(textures)
            button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
            # update the screen
            update_menu = True

            last_touched_mask = None

            while game.loop and game.state == "infos":

                # check events
                event, mask_touching, click = events.check(menu_masks)

                if event is "leave":
                    game.stop()

                if event is "escape":
                    game.state = "menu"

                if event in ["space", "enter"]:
                    open_url('https://github.com/V-def/select-game')

                for touched_mask in mask_touching:

                    if touched_mask[3].startswith("but"):

                        if click:
                            if touched_mask[3] == "but_1":
                                open_url('https://github.com/V-def/select-game')
                            elif touched_mask[3] == "but_2":
                                open_url('http://valentin.cassayre.me/select')
                            elif touched_mask[3] == "but_3":
                                game.state = "menu"
                            elif touched_mask[3] == "but_4":
                                game.stop()

                        elif last_touched_mask is not touched_mask[3]:
                            button = disp.draw_surface(textures.dflt["button_overlay"],
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
                game.clock.tick(c.FPS)

        # interrupt
        if game.loop and game.state == "interrupt":

            # initialize the menu
            # use disp class to draw the menu page
            menu_masks, bg_surface, texts_surface = disp.create_interrupt_menu(textures)
            button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
            # update the screen
            update_menu = True

            last_touched_mask = None

            while game.loop and game.state == "interrupt":

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
                                game.stop()
                            elif touched_mask[3] == "but_4":
                                open_url('https://github.com/V-def/select-game')

                        elif last_touched_mask is not touched_mask[3]:
                            button = disp.draw_surface(textures.dflt["button_overlay"],
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
                game.clock.tick(c.FPS)

        # game
        if game.loop and game.state == "game" or game.state == "tutorial":

            disp.draw_screen()
            disp.draw_surface(textures.game["board"], c.CENTER, False)
            update_board = True
            game.start_clock()

            selected_insect = None
            drag = False

            in_game_button, in_game_button_mask = disp.draw_in_game_buttons(textures)
            end_game_button, end_game_button_mask = disp.draw_end_game_buttons(textures)

            last_update = pygame.time.get_ticks()

            # initialize the game
            if not game.started:

                # prepare the initial position of the insects
                for insect_data in InitialLayout.classic():

                    insect = insect_data[0](insect_data[1], insect_data[2], textures.insect_path)
                    # update tile
                    board.tile(insect.pos, insect)
                    # add the insect to the other
                    game.insects.append(insect)
                    # importing insect texture
                    textures.save_insect(insect.full_name, insect.pict)

                game.update_ways()
                game.started = True

            # real game main loop
            while game.loop and game.state == "game":

                # limit the frame rate
                game.clock.tick(c.FPS)

                # find the event
                event, mask_touching, click = events.check(mask_list=board.mask_list + in_game_button_mask + end_game_button_mask)

                if event == "leave":
                    game.stop()

                if event == "escape":
                    game.state = "interrupt"

                for touched_mask in mask_touching:

                    if touched_mask[3] == "tile":

                        update_board, game.tile_pos = board.draw_tile_overview(touched_mask, textures)

                    elif touched_mask[3] == "takeback":

                        pass

                    elif touched_mask[3] == "offer_draw":

                        if click:

                            game.log = None, "{} offer draw".format(game.turn.capitalize())

                    elif touched_mask[3] == "give_up":

                        if click:

                            game.log = game.turn, "{} gave up !".format(game.turn.capitalize())

                    elif touched_mask[3] == "rematch":

                        if click:

                            print("rematch")

                    elif touched_mask[3] == "return_main_menu":

                        if click:

                            game.state = "menu"

                game.check_end_game()

                if game.process == "next turn":

                    game.process = "choose insect"
                    game.change_turn()
                    game.check_end_game()

                elif game.process == "end game":

                    game.stop_clock()

                # act after a click
                if click:

                    drag = True

                    if game.process == "choose insect":

                        update_board, selected_insect = game.choose_insect(board, textures)

                elif drag and not events.mouse_but_down:

                    if game.process == "choose way":

                        update_board, selected_insect = game.choose_way(board, textures, drag=drag)
                        drag = False

                if last_update//100 != pygame.time.get_ticks()//100:
                    last_update = pygame.time.get_ticks()
                    update_disp = True

                if update_disp:
                    """
                    update everything on the display except the board
                    """
                    disp.draw_screen()

                    # update the screen
                    log_text = str((events.mouse_pos, events.mouse_but_down))
                    log = textures.font["menu button"].render(log_text, True, textures.colors["button_text"])
                    disp.draw_surface(log, c.CENTER, False)

                    # update clock
                    game.update_clock()

                    # buttons
                    disp.draw_surface(in_game_button, c.CENTER, False)
                    disp.draw_surface(end_game_button, c.CENTER, False)

                    disp.draw_table(game.last_turn, game.turn, game.process, game.player_clock, textures)

                    if game.log is not None:
                        disp.game_over(game.log[1], textures)

                    update_board = True

                    game.clock.tick(c.FPS)

                if update_board:
                    """
                    update only the board
                    """

                    # draw the board to erase old position of the insects for the next update
                    disp.draw_surface(textures.game["board"], c.MIDDLE)

                    # draw the ways_surface
                    disp.draw_surface(board.ways_surface, c.CENTER, False)

                    # draw last move
                    disp.draw_surface(board.last_move_surface, c.CENTER, False)

                    # draw setback
                    if game.setback is not None:
                        disp.draw_surface(textures.game['tile_setback'], board.position(game.setback.pos), True)

                    # draw the mouse tile pos
                    disp.draw_surface(board.mouse_interaction_surface, c.CENTER, False)

                    # draw the insects
                    for insect in game.insects:
                        if insect == selected_insect and drag:
                            disp.draw_surface(textures.dflt[insect.full_name], events.mouse_pos)
                        else:
                            disp.draw_surface(textures.dflt[insect.full_name], board.position(insect.pos))

                    game.clock.tick(c.FPS)

                if update_disp or update_board:

                    # update
                    pygame.display.flip()
                    game.clock.tick(c.FPS)

                    update_disp, update_board = False, False


# everything starts here
if __name__ == '__Select__':
    main()
