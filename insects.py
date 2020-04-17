"""
The classes of the insects : How do they move ?
Insects are the pieces of the game
"""
import pygame
import math
from display import *
from consts import *


# this was just some idea not touched since long time
class Insect:
    """
    mother class of all the insects
    """
    def __init__(self, pos, color):
        self.a, self.b = pos
        self.color = color
        self.ways = []

    def _get_position(self):
        return self.a, self.b

    def _set_position(self, new_pos):
        pos = new_pos

    pos = property(_get_position, _set_position)


class Bug(Insect):
    """
    The bug is an insect
    """
    def __init__(self, pos, color):
        Insect.__init__(self, pos, color)
        self.pict = pygame.image.load(BUG_PATH)

    def highlight_ways(self):
        if self.color == "White":
            # All the ways this insect can go
            self.ways = [(self.a + 1, self.b), (self.a, self.b), (self.a + 1, self.b + 1)]
            for coord in self.ways:
                self.p_a, self.p_b = coord
                self.highlight = Board().highlight_hexagon(Board().coords(self.p_a, self.p_b))


