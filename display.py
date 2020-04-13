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
        self.draw = self.screen.blit(picture, pos)

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

    def coords(self, x, y):
        """
        create the coordinates of the 6 points of the hexagone
        :param x: x coord
        :param y: y coord
        :return: list of coords (tuplets)
        """
        coords = []
        for k in range(6):
            coords.append((x + RADIUS * math.cos(k * math.pi / 3), y + RADIUS * math.sin(k * math.pi / 3)))
        self.coordinate_list = coords
        return coords

    def draw_hexagon(self, color, coords):
        self.hexagon = pygame.draw.polygon(self.screen, color, coords)

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
                    self.draw_hexagon(color, self.coords(x, y))
