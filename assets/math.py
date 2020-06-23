# -*- coding: utf-8 -*-

"""
custom math module made for this game and to help calculate hexagons
"""


class Math:

    @staticmethod
    def sqrt(x):
        return x**0.5

    @staticmethod
    def inscribed_rad(radius):
        """
        radius of the inscribed circle that contain the sides of the hexagon from a circumscribed circle radius
        """
        return Math.sqrt(3)*radius/2
