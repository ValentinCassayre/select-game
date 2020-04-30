"""
check events (mouse, keyboard, leave etc)
"""

import pygame


class Events:

    def __init__(self):
        pass

    @staticmethod
    def check_ev():

        event_str = None

        for event in pygame.event.get():

            if event.type is pygame.QUIT:
                event_str = "leave"

            elif event.type is pygame.KEYDOWN:

                if event.key is pygame.K_ESCAPE:
                    event_str = "escape"

                if event.key is pygame.K_SPACE:
                    event_str = "space"

                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    event_str = "return"

        return event_str
