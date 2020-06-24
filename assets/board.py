# -*- coding: utf-8 -*-

"""
Board
"""

import pygame
import assets.consts as c
from assets.display import Display


class Board(Display):
    """
    Class about everything related to the board
    """

    def __init__(self):
        """
        Constructor
        """
        Display.__init__(self)
        self.coordinate_list = []
        self.pos_list = []
        self.disp_list = []
        self.mask_list = []
        self.tile_state = {}

        self.ways = {}
        self.eat = {}

        self.last_tile_pos = None

        self.draw_ways = True  # if false the game will no longer display the ways each insect can go

        self.to_draw = {'last move': None, 'ways': None, 'setback': None}

        self.screen_copy = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.mouse_interaction_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.ways_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.last_move_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.setback_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        # find were to draw the board to fit in the middle
        self.board_origin = c.X_MID, (c.Y_SIZE-self.position((9, 9), origin=(0, 0))[1])/2

    def __copy__(self):
        """
        copy board
        """
        new_board = type(self)()
        new_board.__dict__.update(self.__dict__)
        return new_board

    def _get_last_tile(self):
        return self.last_tile_pos

    def _set_last_tile(self, pos):
        self.last_tile_pos = pos

    last_tile = property(_get_last_tile, _set_last_tile)

    def position(self, b_pos, origin=None):
        """
        convert position coordinates of the board from an orthonormal system to the specific system of the screen
        convert position from board (b_pos) to screen coordinate x, y (coords)
        """
        if origin is None:
            origin = self.board_origin
        a, b = b_pos
        xo, yo = origin
        x = xo + (a * 3 * c.R / 2 - b * 3 * c.R / 2) * c.MULT
        y = yo + (a * c.U + b * c.U) * c.MULT
        return x, y

    def create_board(self, color_bg, tile_1, tile_2, tile_mask):

        # create a list of all the possible position of the board under the form of tuple (x, y)
        # creating a 10 by 10 board

        image = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA)

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
                    disp_pos = self.position(cell)

                    if i % 5 == 2 or j % 5 == 2:
                        self.draw_surface(draw_this_surface=tile_1, disp_pos=disp_pos, on_this_surface=image)
                    else:
                        self.draw_surface(draw_this_surface=tile_2, disp_pos=disp_pos, on_this_surface=image)

                    self.pos_list.append(cell)
                    self.disp_list.append(disp_pos)

                    # create masks to detect if the mouse interact with the tiles
                    self.mask_list.append(self.convert_to_mask(tile_mask, disp_pos, "tile", b_pos=cell))

                    # create dict of all the states of the cells, by default False (no insect on it)
                    self.tile_state.update({cell: None})
        return image

    def tile(self, new_pos, insect, update_insect=True):
        """
        give the state_string of a tile, pos = (x, y) and insect = True if the tile is insect
        """
        self.tile_state.update({new_pos: insect})
        if insect is not None and update_insect:
            insect.pos = new_pos

    def check_tile_move(self, insect_moving, new_pos):
        """
        check if the insect can go on this tile without his ant beeing attacked
        """
        pass

    def reset_surface(self, name):
        if name == 'mouse interaction surface':
            self.mouse_interaction_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        elif name == 'ways':
            self.ways_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        elif name == 'last move':
            self.last_move_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        elif name == 'setback':
            self.setback_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

    def draw_tile_overview(self, mask_infos, textures):

        update = False
        disp_pos = mask_infos[2]
        tile_pos = mask_infos[4]

        # check if the tile is a new tile, else no update of the screen
        if self.last_tile != mask_infos[4]:
            self.reset_surface("mouse interaction surface")
            self.draw_surface(draw_this_surface=textures.game["tile overview"], disp_pos=disp_pos,
                              on_this_surface=self.mouse_interaction_surface)

            update = True
        self.last_tile_pos = mask_infos[4]

        return update, tile_pos

    def draw_last_move(self, pos_list, textures):

        # clean last move
        self.last_move_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        # add both pos of new move
        for pos in pos_list:
            self.draw_surface(draw_this_surface=textures.game["tile move"], disp_pos=self.position(pos),
                              on_this_surface=self.last_move_surface)

    def game_draw(self, category, data, textures):
        """
        draw stuff on board asked by game object
        data : (name for texture.game[name], board position, 'surface id')
        """

        for tile in data:
            name, board_pos, surface_name = tile
            pos = self.position(board_pos)

            if surface_name == 'ways surface':
                surface = self.ways_surface

            elif surface_name == 'eat surface':
                surface = self.ways_surface

            elif surface_name == 'last move surface':
                surface = self.last_move_surface

            elif surface_name == 'last kill surface':
                surface = self.last_move_surface

            elif surface_name == 'setback surface':
                surface = self.setback_surface

            else:
                surface = None

            if surface is not None:
                self.to_draw[category] = self.draw_surface(draw_this_surface=textures.game[name], disp_pos=pos,
                                                           on_this_surface=surface, center=True)

    def render(self, board_render, textures):

        image = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        # draw the board to erase old position of the insects for the next update
        self.draw_surface(textures.game["board"], image, c.MIDDLE)

        # draw the insects
        for tile in board_render:
            if board_render[tile] is not None:
                insect = board_render[tile]
                self.draw_surface(textures.dflt[insect.full_name], image, self.position(tile))

        return image

