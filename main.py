"""
Prototype game by Valentin Cassayre
Git : https://github.com/V-def/select-game
"""

import pygame
import math
from consts import *
from display import *
from insects import *


def main():
    # Pygame initialization
    pygame.init()
    disp = PyDisp()
    board = Board()

    # Windows first settings
    pygame.display.set_caption(GAME_NAME)

    # Variables
    main_loop = True
    game_started = False
    state = "menu"
    game_state = "not started"
    turn = "white"

    disp.draw_screen()

    # insects of the board initial pos
    a1 = Bug((0, 0), "white")

    # loop while game is open
    while main_loop:

        if main_loop and state == "menu":
            game_started = False
            disp.draw_menu()

            pygame.display.flip()

            while main_loop and state == "menu":
                ORIGIN = (X_SIZE // 2, Y_SIZE // 2)
                hexa_coords = board.coords(ORIGIN[0], ORIGIN[1])
                pygame.draw.polygon(disp.screen, BLACK, hexa_coords, 1)

                Rectplace_RED = pygame.draw.rect(disp.screen, RED,
                                             (hexa_coords[3][0], hexa_coords[4][1], RADIUS*2+1, UNIT+1), 1)

                Rectplace_GREEN = pygame.draw.rect(disp.screen, GREEN,
                                             (hexa_coords[4][0], hexa_coords[4][1], RADIUS + 1, UNIT + 1), 1)

                image = pygame.image.load("hex.png")

                # Mouse position and button clicking.
                pos = pygame.mouse.get_pos()
                x, y = pos
                pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
                # Check if the rect collided with the mouse pos
                # and if the left mouse button was pressed.
                if Rectplace_RED.collidepoint(pos) and pressed1:
                    if Rectplace_GREEN.collidepoint(pos) and pressed1:
                        print("HEX -> GREEN_RECT")
                    elif y < 2*x - 789:
                        print("NOT HEX -> RED_RECT_CORNER_LEFT_UP")
                    else:
                        print("HEX -> RED_RECT_NOT_CORNER")

                pygame.display.flip()

                # check mouse and keyboard
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main_loop = False
                    elif event.type == pygame.KEYDOWN:
                        # close windows
                        if event.key == pygame.K_ESCAPE:
                            main_loop = False
                        # enter game
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            state = "game"

                disp.clock.tick(FPS)

        if main_loop and state == "game":
            # Start the game
            if not game_started:
                disp.game_start()
                board.draw_board()
                game_state = "choose insect"
                # need to add draw insects

                game_started = True

            while main_loop and state == "game":
                # draw the board
                board.draw_board()
                # draw the insects
                pos = board.position((0, 0))
                bug1 = Bug(pos, COLOR_HIGHLIGHT)
                disp.draw_insect(bug1.pict, pos)

                mouse_pos = pygame.mouse.get_pos()
                board.click_on_hexagon(mouse_pos)
                x, y = mouse_pos
                a, b = board.screen_position(x, y)
                c, d = board.position((a, b))
                coords = board.coords(c, d)
                board.draw_hexagon(BLUE, coords, coords)

                # get all events
                ev = pygame.event.get()

                pygame.display.flip()

                disp.clock.tick(FPS)

                for event in ev:
                    if event.type == pygame.QUIT:
                        main_loop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            state = "interrupt"

                if turn == "white":

                    if game_state == "choose insect":
                        pass
                    if game_state == "finished":
                        game_state = "choose insect"
                        turn = "black"
                        disp.clock.tick(FPS)

                if turn == "black":
                    turn = "white"
                    disp.clock.tick(FPS)

            if main_loop and state == "interrupt":
                """
                Need to add this
                """
                main_loop = False


# everything starts here
if __name__ == '__main__':
    main()
