"""
Stuff for displaying stuff
"""

import pygame

from assets.insects import *
from assets.textures import *


class PyDisp:
    """
    Display mother class
    """
    def __init__(self):
        """
        Constructor
        """
        # name the window
        pygame.display.set_caption(GAME_NAME)
        # add an icon
        pygame.display.set_icon(pygame.image.load(ICON))
        # Create a python surface for the screen
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        # Create the clock used to control the frame rate
        self.clock = pygame.time.Clock()

    def draw_screen(self):
        """
        Create white background on the screen
        """
        self.screen.fill(BACKGROUND_COLOR)

    def draw_menu(self):
        """
        Draw the menu screen
        """
        # Need to add the menu textures
        self.draw_screen()

    def draw_surface(self, image, surface, disp_pos, center=True):
        """
        draw a surface centered in the given coords
        """
        x, y = disp_pos
        if center:
            image.blit(surface, (x - surface.get_width() // 2, y - surface.get_height() // 2))
        else:
            image.blit(surface, (x, y))
        return image


class Board(PyDisp):
    """
    Class about everything related to the board
    """

    def __init__(self):
        """
        Constructor
        """
        PyDisp.__init__(self)
        self.coordinate_list = []
        self.pos_list = []
        self.disp_list = []
        self.mask_list = []
        self.tile_state = {}

        self.screen_copy = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self.mouse_interaction_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.ways_surface = self.screen_copy

    def mask_hexagon(self, mask_surface, b_pos):
        """
        create and return the mask of a tile with the position of the tile in the display and not in the board
        """
        x, y = self.position(b_pos)
        tile_rect = mask_surface.get_rect(center=(x, y))
        # place mask itself
        tile_mask = pygame.mask.from_surface(mask_surface)
        return tile_rect, tile_mask, (x, y), b_pos

    def position(self, b_pos, xo=B_XO, yo=B_YO):
        """
        convert position coordinates of the board from an orthonormal system to the specific system of the screen
        convert position from board (b_pos) to screen coordinate x, y (coords)
        """
        a, b = b_pos
        x = xo + (a*3*RADIUS/2 - b*3*RADIUS/2)*EDGE_WIDTH
        y = yo + (a*UNIT/2 + b*UNIT/2)*EDGE_WIDTH
        return x, y

    def create_board(self, color_bg, tile_1, tile_2, tile_mask):

        # create a list of all the possible position of the board under the form of tuple (x, y)
        # creating a 10 by 10 board

        image = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        coords_bg = [self.position((4, 0)), self.position((0, 0)), self.position((0, 4)),
                     self.position((5, 9)), self.position((9, 9)), self.position((9, 5))]

        pygame.draw.polygon(image, color_bg, coords_bg)

        for i in range(10):
            for j in range(10):
                # remove unwanted cell in the corners
                if abs(j - i) >= 5:
                    continue
                # adding the right cells to the board (70 in total)
                else:
                    cell = i, j
                    disp_pos = self.position(cell, MIDDLE[0])

                    if i % 5 == 2 or j % 5 == 2:
                        self.draw_surface(image, tile_1, disp_pos)
                    else:
                        self.draw_surface(image, tile_2, disp_pos)

                    self.pos_list.append(cell)
                    self.disp_list.append(disp_pos)

                    # create masks to detect if the mouse interact with the tiles
                    self.mask_list.append(self.mask_hexagon(tile_mask, cell))

                    # create dict of all the states of the cells, by default False (no insect on it)
                    self.tile_state.update({cell: False})
        return image

    def tile(self, b_pos, taken):
        """
        give the state of a tile, pos = (x, y) and taken = True if the tile is taken
        """
        self.tile_state.update({b_pos: taken})

    def reset_surface(self, name):
        if name == "mouse_interaction_surface":
            self.mouse_interaction_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
        elif name == "ways_surface":
            self.ways_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        else:
            print("Error")
