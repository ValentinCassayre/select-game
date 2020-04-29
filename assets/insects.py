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

    def kill(self, insect_killed):
        self.position = insect_killed.pos
        insect_killed.killed()

    def killed(self):
        del self

class Bug(Insect):
    """
    the smallest insect
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
            for i in range(1, 2):  # -> range of one
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

        return directions_way, directions_eat, False


class Locust(Insect):
    """
    the insect that can jump
    """
    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "locust"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self):
        # (ways, eat) both are directions list composed by direction
        # this insect ways does not depends of its color

        # ways
        directions_way = [[(self.a + 2, self.b)], [(self.a, self.b + 2)], [(self.a + 2, self.b + 2)],
                          [(self.a - 2, self.b)], [(self.a, self.b - 2)], [(self.a - 2, self.b - 2)]]

        # eat
        directions_eat = [[(self.a + 2, self.b)], [(self.a, self.b + 2)], [(self.a + 2, self.b + 2)],
                          [(self.a - 2, self.b)], [(self.a, self.b - 2)], [(self.a - 2, self.b - 2)]]

        return directions_way, directions_eat, False


class Spider(Insect):
    """
    the insect that can go on the sides
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "spider"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self):
        # this insect ways does not depends of its color
        # ways
        directions_way = []
        direction = []
        for i in range(1, 10):
            direction.append((self.a + i, self.b))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((self.a, self.b + i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((self.a - i, self.b))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((self.a, self.b - i))
        directions_way.append(direction)

        # eat
        directions_eat = []
        # this insect can only eat insect who are at the end of the ways range and this is calculated by the board class

        return directions_way, directions_eat, True


class Beetle(Insect):
    """
    the insect that can go on the front
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "beetle"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self):
        # (ways, eat) both are directions list composed by direction

        # ways
        # sides
        directions_way = [[(self.a + 1, self.b)], [(self.a, self.b + 1)],
                          [(self.a - 1, self.b)], [(self.a, self.b - 1)]]

        # front
        direction = []
        for i in range(1, 10):
            direction.append((self.a + i, self.b + i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((self.a - i, self.b - i))
        directions_way.append(direction)

        # eat
        directions_eat = []
        # this insect can only eat insect who are at the end of the ways range and this is calculated by the board class

        return directions_way, directions_eat, True


class Bee(Insect):
    """
    the insect that can everywhere but die if it kill another insect
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "bee"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self):
        # (ways, eat) both are directions list composed by direction

        # ways
        directions_way = []
        direction = []
        for i in range(1, 10):
            direction.append((self.a + i, self.b + i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((self.a - i, self.b - i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((self.a + i, self.b))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((self.a, self.b + i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((self.a - i, self.b))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((self.a, self.b - i))
        directions_way.append(direction)

        # eat
        directions_eat = []
        # this insect can only eat insect who are at the end of the ways range and this is calculated by the board class

        return directions_way, directions_eat, True


class Ant(Insect):
    """
    this is the main insect : other insects needs to protect it
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "ant"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self):
        # (ways, eat) both are directions list composed by direction

        directions_way = [[(self.a + 1, self.b)], [(self.a, self.b + 1)],
                          [(self.a - 1, self.b)], [(self.a, self.b - 1)]]

        # eat
        directions_eat = directions_way

        return directions_way, directions_eat, False


class Custom(Insect):
    """
    this is a bonus insect you can change parameters
    """
    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "custom"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self):
        # (ways, eat) both are directions list composed by direction

        if self.color == "white":
            # ways that mean the insect can only go if there is nobody on these tile
            directions_way = []

            # one of the direction the insect can go
            # each direction is stopped by the first opponent they see
            direction = []
            for i in range(1, 2):  # -> range in which the insect can go
                direction.append((self.a + i, self.b + i))
            # add it to the other directions
            directions_way.append(direction)

            # other direction this insect can go
            direction = []
            for i in range(1, 3):
                direction.append((self.a + i, self.b))
            # add it to the other directions
            directions_way.append(direction)

            # other direction this insect can go
            direction = []
            for i in range(1, 3):
                direction.append((self.a, self.b + i))
            # add it to the other directions
            directions_way.append(direction)

            # eat that mean the insect can only go if there is an opponent on these tile
            directions_eat = []

            direction = []
            for i in range(1, 2):  # -> range in which the insect can eat
                direction.append((self.a - i, self.b - i))
            # add it to the other directions
            directions_eat.append(direction)

            direction = []
            for i in range(1, 3):  # -> range in which the insect can eat
                direction.append((self.a - i, self.b))
            # add it to the other directions
            directions_eat.append(direction)

            direction = []
            for i in range(1, 3):  # -> range in which the insect can eat
                direction.append((self.a, self.b - i))
            # add it to the other directions
            directions_eat.append(direction)

        else:  # black

            # ways that mean the insect can only go if there is nobody on these tile
            directions_way = []

            # one of the direction the insect can go
            # each direction is stopped by the first opponent they see
            direction = []
            for i in range(1, 2):  # -> range in which the insect can go
                direction.append((self.a - i, self.b - i))
            # add it to the other directions
            directions_way.append(direction)

            # other direction this insect can go
            direction = []
            for i in range(1, 3):
                direction.append((self.a - i, self.b))
            # add it to the other directions
            directions_way.append(direction)

            # other direction this insect can go
            direction = []
            for i in range(1, 3):
                direction.append((self.a, self.b - i))
            # add it to the other directions
            directions_way.append(direction)

            # eat that mean the insect can only go if there is an opponent on these tile
            directions_eat = []

            direction = []
            for i in range(1, 2):  # -> range in which the insect can eat
                direction.append((self.a + i, self.b + i))
            # add it to the other directions
            directions_eat.append(direction)

            direction = []
            for i in range(1, 3):  # -> range in which the insect can eat
                direction.append((self.a + i, self.b))
            # add it to the other directions
            directions_eat.append(direction)

            direction = []
            for i in range(1, 3):  # -> range in which the insect can eat
                direction.append((self.a, self.b + i))
            # add it to the other directions
            directions_eat.append(direction)

        return directions_way, directions_eat, False
