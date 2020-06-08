"""
Display
"""

import pygame
from assets.display import Display
import assets.consts as c


class Board(Display):
    """
    Class about everything related to the board
    """

    def __init__(self):
        """
        Constructor
        """
        Display.__init__(self)
