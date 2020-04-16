"""
Stuff for displaying stuff
"""

import pygame
import math
from insects import *
from consts import *


class PyDisp:
    """
    Display class
    """
    def __init__(self):
        """
        Constructor
        """
        # Create a python surface for the screen
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        # Create the clock used to control the frame rate
        self.clock = pygame.time.Clock()

    def draw_screen(self):
        self.screen.fill(BACKGROUND_COLOR)

    def draw_menu(self):
        """
        Draw the menu screen
        """
        pass

    def game_start(self):
        pass

    def draw_insect(self, picture, pos):
        """
        Draw the insects
        """
        self.picture_rect = picture.get_rect()
        self.picture_rect.center = pos
        self.draw = self.screen.blit(picture, self.picture_rect)

"""
Special class for the board
"""


class Board(PyDisp):
    """
    Class to draw the cells of the board
    """

    def __init__(self):
        """
        Class builder
        """
        PyDisp.__init__(self)
        self.coordinate_list = []
        self.sprites = []

        # prepare for the tile to be clickable
        self.tile = pygame.image.load("hex.png").convert_alpha()
        self.rect = self.tile.get_rect()
        self.tile_mask = pygame.mask.from_surface(self.tile)
        self.mask_list = []

    def coords(self, x, y, width = 1.0):
        """
        create the coordinates of the 6 points of the hexagone
        :param x: x coord
        :param y: y coord
        :return: list of coords (tuplets)
        """
        coords = []
        for k in range(6):
            coords.append((x + width * RADIUS * math.cos(k * math.pi / 3), y + width * RADIUS * math.sin(k * math.pi / 3)))
        self.coordinate_list = coords
        return coords

    def draw_hexagon(self, color, coords_draw, coords_fill):
        # draw edges
        self.hexagon_edges = pygame.draw.polygon(self.screen, COLOR_EDGE1, coords_draw)
        # fill hexagon
        self.hexagon = pygame.draw.polygon(self.screen, color, coords_fill)

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
        self.highlight_hexagon = pygame.draw.polygon(self.screen, COLOR_HIGHLIGHT, coords)

    def position(self, board_pos):
        """
        Convert position coordinates of the board from an orthonormal system to the specific system
        """
        self.a, self.b = board_pos
        x = X_BASE + (self.a*3*RADIUS/2 - self.b*3*RADIUS/2)*1.1
        y = Y_BASE + (self.a*UNIT/2 + self.b*UNIT/2)*1.1
        return x, y

    def draw_board(self):
        for i in range(10):
            for j in range(10):
                if j-i >= 5 or i-j >=5:
                    continue
                else:
                    color = COLOR_TILE1
                    (x, y) = self.position((i, j))
                    if i % 5 == 2 or j % 5 == 2:
                        color = COLOR_TILE2
                    self.draw_hexagon(color, self.coords(x, y, 1.2), self.coords(x, y))
                    self.mask_list.append(self.mask_hexagon(x, y))

    def raw(self):
        # something to find the different raw
        raw_list = []
        for i in range(4):
            a, b = self.position((0, 4 - i))
            pos = self.coords(a, b)[3][0]
            raw_list.append(pos)
        for i in range(5):
            a, b = self.position((i, 0))
            pos = self.coords(a, b)[0][0]
            raw_list.append(pos)
        return raw_list

    def click_on_hexagon(self, cursor_pos):
        x, y = cursor_pos
        raw = self.raw()

    def screen_position(self, x, y):
        a = (2*(x-X_BASE)/(3*1.1*RADIUS)) + ((y-Y_BASE)/(1.1*UNIT))
        b = ((y - Y_BASE)/(1.1*UNIT)-2*(x-X_BASE)/(3*1.1*RADIUS))
        return int(round(a)), int(round(b))
