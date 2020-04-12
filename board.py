"""
Everything related to the board ans the cells
"""

import math
import pygame
from insects import *
from consts import *


class Cell():
    """
    Class to draw the cells
    """

    def __init__(self):
        """
        Class builder
        """

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
        return coords
"""
    def draw_hexagon(self, coords):
        pygame.draw.polygon(screen, COLOR_TILE1, coords)"""

