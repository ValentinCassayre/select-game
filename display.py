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
        # add a logo
        # -------------
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
        self.sprites = []

        # prepare for the tile to be clickable
        self.tile = pygame.image.load("hex.png").convert_alpha()
        self.rect = self.tile.get_rect()
        self.tile_mask = pygame.mask.from_surface(self.tile)
        self.mask_list = []

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
            coords.append((x + width * RADIUS * math.cos(k * math.pi / 3), y + width * RADIUS * math.sin(k * math.pi / 3)))
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

    def mask_hexagon(self, x, y):
        """
        create and return the mask of a tile with the position of the tile in the board
        """
        # convert coordinates of the board into coordinates of the screen
        a, b = self.position((x, y))
        # place mask itself
        self.rect = self.tile.get_rect(center=(a, b))
        self.tile_mask = pygame.mask.from_surface(self.tile)
        return self.rect, self.tile_mask

    def highlight_hexagon(self, coords):
        pygame.draw.polygon(self.screen, COLOR_HIGHLIGHT, coords)

    def position(self, board_pos):
        """
        convert position coordinates of the board from an orthonormal system to the specific system of the screen
        convert position from board to screen coordinate x, y
        """
        a, b = board_pos
        x = X_BASE + (a*3*RADIUS/2 - b*3*RADIUS/2)*1.1
        y = Y_BASE + (a*UNIT/2 + b*UNIT/2)*1.1
        return x, y

    def draw_board(self):
        """
        draw the game board
        """
        for i in range(10):
            for j in range(10):
                if j-i >= 5 or i-j >= 5:
                    continue
                else:
                    (x, y) = self.position((i, j))
                    if i % 5 == 2 or j % 5 == 2:
                        color = COLOR_TILE2
                    else:
                        color = COLOR_TILE1
                    self.draw_hexagon((x, y), color)
                    self.mask_list.append(self.mask_hexagon(x, y))

    def click_on_hexagon(self, cursor_pos):
        x, y = cursor_pos

        return

    def draw_insect(self, picture, pos):
        """
        Draw the insects
        """
        # need to complete this bad boy these a just ideas
        self.picture_rect = picture.get_rect()
        self.picture_rect.center = pos
        self.draw = self.screen.blit(picture, self.picture_rect)
