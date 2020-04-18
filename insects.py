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
        self.eat = []

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

    def ways(self):
        if self.color == "white":
            # all the ways this insect can go if nothing on new tile
            self.ways = [(self.a + 1, self.b + 1)]
            # if there is an insect it can eat, he can go there and eat it
            self.eat = [(self.a + 1, self.b), (self.a, self.b + 1)]
        if self.color == "black":
            # All the ways this insect can go if nothing on new tile
            self.ways = [(self.a - 1, self.b - 1)]

