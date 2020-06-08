"""
Main program file
"""

from os import system

try:
    import pygame
except ModuleNotFoundError:
    print("- Missing Pygame module, try pip install Pygame")
    system("pause")
    exit()

import assets.consts as c
from assets.events import Events
from assets.display import Display
from assets.board import Board
from assets.textures import Textures
from assets.game import Game
from assets.initial_layout import InitialLayout


def main():
    # pygame initialization
    pygame.init()


# everything starts here
if __name__ == '__Select__':
    main()
