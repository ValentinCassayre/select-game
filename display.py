"""
Stuff for displaying stuff
"""

import pygame
import math
from insects import *
from consts import *


class PyDisp:
    """
    Display mother class
    """
    def __init__(self):
        """
        Constructor
        """
        # name the window
        pygame.display.set_caption(GAME_NAME)
        # add an icon
        pygame.display.set_icon(pygame.image.load(ICON))
        # Create a python surface for the screen
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        # Create the clock used to control the frame rate
        self.clock = pygame.time.Clock()

    def draw_screen(self):
        """
        Create white background on the screen
        """
        self.screen.fill(BACKGROUND_COLOR)

    def draw_menu(self):
        """
        Draw the menu screen
        """
        # Need to add something here i think
        self.draw_screen()

    def game_start(self):
        """
        Draw the game ?
        """
        pass


class Board(PyDisp):
    """
    Class about everything related to the board
    """

    def __init__(self):
        """
        Constructor
        """
        PyDisp.__init__(self)
        self.coordinate_list = []
        self.pos_list = []
        self.mask_list = []
        self.tile_state = {}

        # create a list of all the possible position of the board under the form of tuple (x, y)
        # creating a 10 by 10 board
        for i in range(10):
            for j in range(10):
                # remove unwanted cell in the corners
                if abs(j - i) >= 5:
                    continue
                # adding the right cells to the board (70 in total)
                else:
                    self.pos_list.append((i, j))

        for tile_pos in self.pos_list:
            self.tile_state[tile_pos] = False

        # prepare for the tile to be clickable
        self.tile_pict = pygame.image.load(TILE_MASK_PATH).convert_alpha()
        self.tile_rect = self.tile_pict.get_rect()
        self.tile_mask = pygame.mask.from_surface(self.tile_pict)

    def coords(self, pos, width=1.0):
        """
        create the coordinates of the 6 points of the hexagon calculated with the pi/3 modulo
        pos is a tuple of the coordinates on the screen and not on the board
        to convert position from board to screen use position()
        :return: list of coords (tuples)
        """
        x, y = pos
        coords = []
        for k in range(6):
            coords.append((x + width * RADIUS * math.cos(k * math.pi / 3),
                           y + width * RADIUS * math.sin(k * math.pi / 3)))
        self.coordinate_list = coords
        return coords

    def draw_hexagon(self, board_pos, color_fill=COLOR_TILE1, color_outline=COLOR_OUTLINE):
        """
        draw an hexagon on the board position tuple (x, y) with 2 colors, one for the outline and one for the hexagon
        default : draw with the color of the board
        """
        # draw edges
        pygame.draw.polygon(self.screen, color_outline, self.coords(board_pos, 1.2))
        # fill hexagon
        pygame.draw.polygon(self.screen, color_fill, self.coords(board_pos))

    def mask_hexagon(self, a, b):
        """
        create and return the mask of a tile with the position of the tile in the display and not in the board
        """
        x, y = self.position((a, b))
        # place mask itself
        self.tile_rect = self.tile_pict.get_rect(center=(x, y))
        self.tile_mask = pygame.mask.from_surface(self.tile_pict)
        return self.tile_rect, self.tile_mask, (x, y), (a, b)

    def highlight_hexagon(self, coords, click):
        """
        highlight the hexagon in this position
        """
        if click:
            pygame.draw.polygon(self.screen, RED, coords)
        else:
            pygame.draw.polygon(self.screen, COLOR_HIGHLIGHT, coords)

    def position(self, board_pos):
        """
        convert position coordinates of the board from an orthonormal system to the specific system of the screen
        convert position from board to screen coordinate x, y
        """
        a, b = board_pos
        x = X_BASE + (a*3*RADIUS/2 - b*3*RADIUS/2)*1.15
        y = Y_BASE + (a*UNIT/2 + b*UNIT/2)*1.15
        return x, y

    def draw_board(self):
        """
        draw the game board
        """
        for pos in self.pos_list:
            i, j = pos
            x, y = self.position(pos)
            if i % 5 == 2 or j % 5 == 2:
                color = COLOR_TILE2
            else:
                color = COLOR_TILE1
            self.draw_hexagon((x, y), color)
            # creating a mask for each cell
            self.mask_list.append(self.mask_hexagon(i, j))

    def copy_surface(self):
        """
        create a copy of the current surface
        """
        return self.screen.copy()

    def click_on_hexagon(self, cursor_pos):
        x, y = cursor_pos
        return

    def draw_insect(self, image, pos):
        """
        Draw the insects
        """
        # convert pos into coords for the screen
        coords = self.position(pos)
        # need to complete this bad boy these a just ideas
        image_rect = image.get_rect()
        image_rect.center = coords
        self.screen.blit(image, image_rect)

    def tile(self, pos, taken):
        """
        give the state of a tile, pos = (x, y) and taken = True if the tile is taken
        """
        self.tile_state.update({pos: taken})
