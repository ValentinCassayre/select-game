"""
All the initial layouts
"""
# import class
from assets.insects import Bug, Locust, Spider, Beetle, Bee, Ant, Custom


class InitialLayout:
    """
    returns layouts
    """

    @staticmethod
    def add_sym(layout, center_sym=True):
        """
        add all the opponent insects in the symmetrical pos
        two possible mods : central symmetry or linear symmetry
        """

        new_layout = []

        for insect_infos in layout:
            i_type = insect_infos[0]
            pos = insect_infos[1]
            color = insect_infos[2]

            new_pos = InitialLayout.reverse_pos(pos, center_sym)
            new_color = InitialLayout.reverse_color(color)

            # append old insect
            new_layout.append(insect_infos)
            # append new insect
            new_layout.append((i_type, new_pos, new_color))

        new_layout = tuple(new_layout)

        return new_layout

    @staticmethod
    def reverse_pos(pos, center_sym=True):
        """
        reverse the pos on the board
        center_sym is by default true but false make a linear symetry
        """
        x, y = pos
        if center_sym:
            return 9 - y, 9 - x
        else:
            return 9 - x, 9 - y

    @staticmethod
    def reverse_color(color):
        """
        change the color
        """
        if color == "white":
            return "black"
        else:
            return "white"

    @staticmethod
    def classic():
        """
        classic game layout
        """

        layout = (Bug, (0, 3), "white"), (Bug, (1, 3), "white"), (Bug, (2, 3), "white"),\
                 (Bug, (3, 0), "white"), (Bug, (3, 1), "white"), (Bug, (3, 2), "white"), (Bug, (3, 3), "white"),\
                 (Locust, (1, 2), "white"), (Locust, (2, 1), "white"),\
                 (Spider, (0, 2), "white"), (Spider, (2, 0), "white"),\
                 (Beetle, (1, 0), "white"), (Beetle, (0, 1), "white"),\
                 (Bee, (1, 1), "white"), (Bee, (2, 2), "white"),\
                 (Ant, (0, 0), "white")

        return InitialLayout.add_sym(layout, True)

    @staticmethod
    def custom():
        """
        custom game layout
        use it to have fun
        """

        layout = (Custom, (3, 2), "white")

        return InitialLayout.add_sym(layout, True)

    @staticmethod
    def tutoriel(n):
        """
        board layouts for the tutorial
        """

        if n == 0:
            pass
        elif n == 1:
            return InitialLayout.add_sym((Bug, (3, 3), "white"), True)
        elif n == 2:
            layout = (Bug, (0, 3), "white"), (Bug, (1, 3), "white"), (Bug, (2, 3), "white"),\
                     (Bug, (3, 0), "white"), (Bug, (3, 1), "white"), (Bug, (3, 2), "white"), (Bug, (3, 3), "white")
            return InitialLayout.add_sym(layout, True)
        elif n == 3:
            layout = (Locust, (1, 2), "white"), (Locust, (2, 1), "white"),\
                     (Bug, (9, 8), "black"), (Bug, (9, 9), "black"), (Bug, (8, 9), "black")
            return layout
        else:
            pass
