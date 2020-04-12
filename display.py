"""
Stuff for displaying stuff
"""

import pygame
import math
from board import *
from insects import *
from consts import *


class PyDisp:
    """
    Display class
    """
    def __init__(self):
        """
        This will be executed everytime PyDisp is used
        """
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
