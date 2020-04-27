"""
The classes of the insects : How do they move ?
Insects are the pieces of the game
"""

from assets.consts import *
from assets.display import *

from assets.textures import *


# this was just some idea not touched since long time
class Insect:
    """
    mother class of all the insects
    """
    def __init__(self, pos, color, path):
        self.position = pos
        self.a, self.b = pos
        self.color = color
        self.path = path
        self.ways = []
        self.eat = []

    def _get_position(self):
        return self.position

    def _set_position(self, new_pos):
        self.position = new_pos

    pos = property(_get_position, _set_position)


class Bug(Insect):
    """
    The bug is an insect
    """
    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "bug"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_ways(self):
        self.a, self.b = self.position
        if self.color == "white":
            # all the ways_surface this insect can go if nothing on new tile
            self.ways = [(self.a + 1, self.b + 1)]
            # if there is an insect it can eat, he can go there and eat it
            self.eat = [(self.a + 1, self.b), (self.a, self.b + 1)]
        if self.color == "black":
            # All the ways_surface this insect can go if nothing on new tile
            self.ways = [(self.a - 1, self.b - 1)]
            # if there is an insect it can eat, he can go there and eat it
            self.eat = [(self.a - 1, self.b), (self.a, self.b - 1)]

        return self.ways, self.eat


class Locust(Insect):
    """
    The locust is another insect
    """
    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "locust"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")