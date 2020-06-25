# -*- coding: utf-8 -*-

"""
Game modes class
"""

import pygame
import assets.consts as c
from assets.game import Game
import random
import pickle


class Offline(Game):
    """
    offline two players
    """

    def __init__(self, board, textures, clock, chat, settings):
        Game.__init__(self, board, textures, clock, chat, settings)
        self.mode = 'offline'


class Computer(Game):
    """
    offline one player
    """

    def __init__(self, board, textures, clock, chat, settings):
        Game.__init__(self, board, textures, clock, chat, settings)
        self.mode = 'computer'
        self.computer = 'black'

    def check(self):
        if self.turn == self.computer:
            self.play = False


class Online(Game):
    """
    online two players
    """

    def __init__(self, board, textures, clock, chat, settings):
        Game.__init__(self, board, textures, clock, chat, settings)
        self.mode = 'online'


class Tutorial(Game):
    """
    tutorial offline one player
    """

    def __init__(self, board, textures, clock, chat, settings):
        Game.__init__(self, board, textures, clock, chat, settings)
        self.mode = 'tutorial'
