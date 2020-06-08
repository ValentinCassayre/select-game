"""
Display
"""

import pygame
import assets.consts as c


class Display:
    """
    display mother class : everything related to things on the screen
    """
    def __init__(self):
        """
        Constructor
        """
        # name the window
        pygame.display.set_caption(c.GAME_NAME)
        # add an icon
        pygame.display.set_icon(pygame.image.load(c.ICON))
        # Create a python surface for the screen
        self.screen = pygame.display.set_mode(c.SCREEN_SIZE)

        self.stopwatch = pygame.Surface((200, 60), pygame.SRCALPHA, 32)


