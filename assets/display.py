# -*- coding: utf-8 -*-

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

        self.caption = c.GAME_NAME

    # basic tools
    def draw_screen(self):
        """
        Create white background on the screen
        """
        self.screen.fill(c.BACKGROUND_COLOR)

    def draw_surface_screen(self, draw_this_surface, disp_pos=c.CENTER, center=False):
        """
        draw a draw_this_surface centered (or not) in the given coords
        """
        on_this_surface = self.screen

        x, y = disp_pos
        if center:
            on_this_surface.blit(draw_this_surface,
                                 (x - draw_this_surface.get_width() // 2, y - draw_this_surface.get_height() // 2))
        else:
            on_this_surface.blit(draw_this_surface, (x, y))
        return on_this_surface

    def draw_surfaces(self, surface_list, disp_pos=c.MIDDLE, center=True):
        for surface in surface_list:
            self.draw_surface_screen(draw_this_surface=surface, disp_pos=disp_pos, center=center)

    @staticmethod
    def draw_surface(draw_this_surface, on_this_surface, disp_pos=(0, 0), center=True, middle=False):
        """
        draw a draw_this_surface centered (or not) in the given coords
        """
        if middle:
            disp_pos = (on_this_surface.get_width() // 2, on_this_surface.get_height() // 2)

        x, y = disp_pos

        if center:
            on_this_surface.blit(draw_this_surface,
                                 (x - draw_this_surface.get_width() // 2, y - draw_this_surface.get_height() // 2))
        else:
            on_this_surface.blit(draw_this_surface, (x, y))

        return on_this_surface

    @staticmethod
    def convert_to_mask(mask_surface, disp_pos, type_name, b_pos=None):
        """
        create and return the mask of a tile with the position of the tile in the display and not in the board
        """
        x, y = disp_pos
        tile_rect = mask_surface.get_rect(center=(x, y))
        # place mask itself
        tile_mask = pygame.mask.from_surface(mask_surface)
        return tile_rect, tile_mask, (x, y), type_name, b_pos

    # game related

    def big_log(self, text, textures):

        if text is not None:

            rend_text = textures.font["default"].render(text, True, textures.colors["button text"])
            self.draw_surface_screen(rend_text, (c.X_MID, c.Y_SIZE / 26), center=True)

    def set_caption(self, caption=c.GAME_NAME):
        """
        set the window caption
        """
        self.caption = caption
        pygame.display.set_caption(caption)


