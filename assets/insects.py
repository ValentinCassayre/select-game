"""
The classes of the insects : How do they move ?
Insects are the pieces of the game
"""

import pygame


class Insect:
    """
    mother class of all the insects
    """

    def __init__(self, pos, color, path):
        self.position = pos
        self.color = color
        self.path = path
        self.ways = []
        self.eat = []
        self.alive = True

        # special perks
        self.king = False
        self.kamikaze = False

    def __del__(self):
        pass

    def _get_position(self):
        return self.position

    def _set_position(self, new_pos):
        self.position = new_pos

    pos = property(_get_position, _set_position)

    @staticmethod
    def kill(insect_killed):
        insect_killed.killed()

    def killed(self):
        self.alive = False
        del self

    def update_directions(self, new_dir):
        self.ways, self.eat = new_dir


class Bug(Insect):
    """
    the smallest insect
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "bug"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self, pos=None):
        # (ways, eat) both are directions list composed by direction

        if pos is None:
            pos = self.position
        a, b = pos

        if self.color == "white":
            # ways
            directions_way = []
            direction = []
            for i in range(1, 2):  # -> range of one
                direction.append((a + i, b + i))
            directions_way.append(direction)

            # eat
            eat = [(a + 1, b), (a, b + 1)]

        else:

            # ways
            directions_way = []
            direction = []
            for i in range(1, 2):
                direction.append((a - i, b - i))
            directions_way.append(direction)

            # eat
            eat = [(a - 1, b), (a, b - 1)]

        return directions_way, eat, False


class Locust(Insect):
    """
    the insect that can jump
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "locust"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self, pos=None):
        if pos is None:
            pos = self.position
        a, b = pos

        # (ways, eat) both are directions list composed by direction
        # this insect ways does not depends of its color

        # ways
        directions_way = [[(a + 1, b + 2)], [(a - 1, b - 2)], [(a + 1, b - 1)],
                          [(a + 2, b + 1)], [(a - 2, b - 1)], [(a - 1, b + 1)]]

        # eat
        eat = [(a + 1, b + 2), (a - 1, b - 2), (a + 1, b - 1), (a + 2, b + 1), (a - 2, b - 1), (a - 1, b + 1)]

        return directions_way, eat, False


class Spider(Insect):
    """
    the insect that can go on the sides
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "spider"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self, pos=None):
        if pos is None:
            pos = self.position
        a, b = pos
        # this insect ways does not depends of its color
        # ways
        directions_way = []
        direction = []
        for i in range(1, 10):
            direction.append((a + i, b))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((a, b + i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((a - i, b))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((a, b - i))
        directions_way.append(direction)

        # eat
        eat = []
        # this insect can only eat insect who are at the end of the ways range and this is calculated by the board class

        return directions_way, eat, True


class Beetle(Insect):
    """
    the insect that can go on the front
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "beetle"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self, pos=None):
        if pos is None:
            pos = self.position
        a, b = pos
        # (ways, eat) both are directions list composed by direction

        # ways
        # sides
        directions_way = [[(a + 1, b)], [(a, b + 1)],
                          [(a - 1, b)], [(a, b - 1)]]

        # front
        direction = []
        for i in range(1, 10):
            direction.append((a + i, b + i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((a - i, b - i))
        directions_way.append(direction)

        # eat
        eat = []
        # this insect can only eat insect who are at the end of the ways range and this is calculated by the board class

        return directions_way, eat, True


class Bee(Insect):
    """
    the insect that can everywhere but die if it kill another insect
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "bee"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")
        self.kamikaze = True

    def calc_directions(self, pos=None):
        if pos is None:
            pos = self.position
        a, b = pos
        # (ways, eat) both are directions list composed by direction

        # ways
        directions_way = []
        direction = []
        for i in range(1, 10):
            direction.append((a + i, b + i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((a - i, b - i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((a + i, b))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((a, b + i))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((a - i, b))
        directions_way.append(direction)
        direction = []
        for i in range(1, 10):
            direction.append((a, b - i))
        directions_way.append(direction)

        # eat
        eat = []
        # this insect can only eat insect who are at the end of the ways range and this is calculated by the board class

        return directions_way, eat, True


class Ant(Insect):
    """
    this is the main insect : other insects needs to protect it
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "ant"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")
        self.king = True

    def calc_directions(self, pos=None):
        if pos is None:
            pos = self.position
        a, b = pos
        # (ways, eat) both are directions list composed by direction

        directions_way = [[(a + 1, b)], [(a, b + 1)],
                          [(a - 1, b)], [(a, b - 1)]]

        # eat
        eat = [(a + 1, b), (a, b + 1),
               (a - 1, b), (a, b - 1)]

        return directions_way, eat, False


class Custom(Insect):
    """
    this is a bonus insect you can change parameters
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "custom"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self, pos=None):
        if pos is None:
            pos = self.position
        a, b = pos
        # (ways, eat) both are directions list composed by direction

        if self.color == "white":
            # ways that mean the insect can only go if there is nobody on these tile
            directions_way = []

            # one of the direction the insect can go
            # each direction is stopped by the first opponent they see
            direction = []
            for i in range(1, 2):  # -> range in which the insect can go
                direction.append((a + i, b + i))
            # add it to the other directions
            directions_way.append(direction)

            # other direction this insect can go
            direction = []
            for i in range(1, 3):
                direction.append((a + i, b))
            # add it to the other directions
            directions_way.append(direction)

            # other direction this insect can go
            direction = []
            for i in range(1, 3):
                direction.append((a, b + i))
            # add it to the other directions
            directions_way.append(direction)

            # eat that mean the insect can only go if there is an opponent on these tile
            directions_eat = []

            direction = []
            for i in range(1, 2):  # -> range in which the insect can eat
                direction.append((a - i, b - i))
            # add it to the other directions
            directions_eat.append(direction)

            direction = []
            for i in range(1, 3):  # -> range in which the insect can eat
                direction.append((a - i, b))
            # add it to the other directions
            directions_eat.append(direction)

            direction = []
            for i in range(1, 3):  # -> range in which the insect can eat
                direction.append((a, b - i))
            # add it to the other directions
            directions_eat.append(direction)

        else:  # black

            # ways that mean the insect can only go if there is nobody on these tile
            directions_way = []

            # one of the direction the insect can go
            # each direction is stopped by the first opponent they see
            direction = []
            for i in range(1, 2):  # -> range in which the insect can go
                direction.append((a - i, b - i))
            # add it to the other directions
            directions_way.append(direction)

            # other direction this insect can go
            direction = []
            for i in range(1, 3):
                direction.append((a - i, b))
            # add it to the other directions
            directions_way.append(direction)

            # other direction this insect can go
            direction = []
            for i in range(1, 3):
                direction.append((a, b - i))
            # add it to the other directions
            directions_way.append(direction)

            # eat that mean the insect can only go if there is an opponent on these tile
            directions_eat = []

            direction = []
            for i in range(1, 2):  # -> range in which the insect can eat
                direction.append((a + i, b + i))
            # add it to the other directions
            directions_eat.append(direction)

            direction = []
            for i in range(1, 3):  # -> range in which the insect can eat
                direction.append((a + i, b))
            # add it to the other directions
            directions_eat.append(direction)

            direction = []
            for i in range(1, 3):  # -> range in which the insect can eat
                direction.append((a, b + i))
            # add it to the other directions
            directions_eat.append(direction)

        eat = []

        return directions_way, eat, False


class God(Insect):
    """
    this is god he can go everywhere
    helpful for tests
    """

    def __init__(self, pos, color, path):
        Insect.__init__(self, pos, color, path)
        self.name = "god"
        self.full_name = self.name + "_" + self.color
        self.pict = pygame.image.load(self.path + self.full_name + ".png")

    def calc_directions(self, pos=None):
        if pos is None:
            pos = self.position
        a, b = pos

        directions_way = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                          (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (3, 1), (3, 2), (3, 3),
                          (3, 4), (3, 5), (3, 6), (3, 7), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                          (4, 7), (4, 8), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
                          (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 3), (7, 4), (7, 5),
                          (7, 6), (7, 7), (7, 8), (7, 9), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (9, 5),
                          (9, 6), (9, 7), (9, 8), (9, 9)]

        eat = directions_way.copy()

        return directions_way, eat, False
