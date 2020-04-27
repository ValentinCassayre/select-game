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
        self.a, self.b = new_pos
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

    def calc_directions(self):
        # (ways, eat) both are directions list composed by direction

        if self.color == "white":
            # ways
            directions_way = []
            direction = []
            for i in range(1, 2):
                direction.append((self.a + i, self.b + i))
            directions_way.append(direction)

            # eat
            directions_eat = []
            direction = []
            for i in range(1, 2):
                direction.append((self.a + i, self.b))
            directions_eat.append(direction)
            direction = []
            for i in range(1, 2):
                direction.append((self.a, self.b + i))
            directions_eat.append(direction)

        else:

            # ways
            directions_way = []
            direction = []
            for i in range(1, 2):
                direction.append((self.a - i, self.b - i))
            directions_way.append(direction)

            # eat
            directions_eat = []
            direction = []
            for i in range(1, 2):
                direction.append((self.a - i, self.b))
            directions_eat.append(direction)
            direction = []
            for i in range(1, 2):
                direction.append((self.a, self.b - i))
            directions_eat.append(direction)

        return directions_way, directions_eat


class Locust(Insect):
    """
    The locust is another insect
    """
    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "locust"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")
