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

        self.stopwatch = pygame.Surface((200, 60), pygame.SRCALPHA, 32)

        self.caption = c.GAME_NAME

    # basic tools
    def draw_screen(self):
        """
        Create white background on the screen
        """
        self.screen.fill(c.BACKGROUND_COLOR)

    def draw_surface_screen(self, draw_this_surface, disp_pos, center=True, on_this_surface=None):
        """
        draw a draw_this_surface centered (or not) in the given coords
        """
        if on_this_surface is None:
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

    def draw_table(self, last_turn, turn, state, clock, textures):
        """
        draw the full table on the right of the screen
        """

        table = self.draw_states(turn, state, textures)

        your_turn = True

        for i in [c.TURN_STATE[turn],  c.TURN_STATE[last_turn]]:

            clock_surface = self.draw_clock(clock=clock[i], turn=your_turn, textures=textures)
            self.draw_surface_screen(draw_this_surface=clock_surface, disp_pos=c.CLOCK[i], on_this_surface=table, center=True)
            your_turn = False

        self.draw_surface_screen(table, c.TB, True)

    def draw_states(self, turn, state, textures):
        """
        on the table draw the states
        """

        table = pygame.Surface(c.TB_SIZE, pygame.SRCALPHA, 32)
        table.fill(textures.colors["infos"])

        self.draw_surface_screen(draw_this_surface=textures.write(turn), disp_pos=c.TURN_P, center=True, on_this_surface=table)
        self.draw_surface_screen(draw_this_surface=textures.write(state, font="game infos"), disp_pos=c.PROCESS_P, center=True,
                                 on_this_surface=table)

        return table

    def draw_clock(self, clock, turn, textures):

        stopwatch = pygame.Surface((200, 60), pygame.SRCALPHA, 32)

        if turn:
            stopwatch.fill(textures.colors["clock turn"])

        else:
            stopwatch.fill(textures.colors["clock not turn"])

        text = pygame.Surface((200, 60), pygame.SRCALPHA, 32)

        seconds = clock // 1000
        minutes = seconds // 60
        hours = minutes // 60

        minutes = minutes - 60 * hours
        seconds = seconds - 60 * minutes - 60**2 * hours
        tenth = "{:03d}".format(clock)[-3]

        # hours
        if hours != 0:
            pos = [20, 30]
            text, pos = self.draw_2_chr(hours, pos, text, textures)
            text, pos = self.draw_small_chr(":", pos, text, textures)
            text, pos = self.draw_2_chr(minutes, pos, text, textures)
            text, pos = self.draw_small_chr(".", pos, text, textures)
            text, pos = self.draw_tenth("{:02d}".format(seconds)[0], pos, text, textures)

        elif minutes == 0 and seconds <= 60:
            pos = [22, 30]
            text, pos = self.draw_2_chr(minutes, pos, text, textures)
            text, pos = self.draw_small_chr(":", pos, text, textures)
            text, pos = self.draw_2_chr(seconds, pos, text, textures)
            text, pos = self.draw_small_chr(".", pos, text, textures)
            text, pos = self.draw_tenth(tenth, pos, text, textures)

        else:
            pos = [46, 30]
            text, pos = self.draw_2_chr(minutes, pos, text, textures)
            text, pos = self.draw_small_chr(":", pos, text, textures)
            text, pos = self.draw_2_chr(seconds, pos, text, textures)

        pos = stopwatch.get_rect().center

        self.draw_surface_screen(text, pos, True, on_this_surface=stopwatch)

        return stopwatch

    def draw_2_chr(self, value, pos, text, textures):
        temp = "{:02d}".format(value)
        for char in temp:
            self.draw_surface_screen(textures.clock_1[char], pos, True, on_this_surface=text)
            pos[0] = pos[0] + 28

        return text, pos

    def draw_small_chr(self, value, pos, text, textures):
        self.draw_surface_screen(textures.clock_1[value], pos, True, on_this_surface=text)
        pos[0] = pos[0] + 20

        return text, pos

    def draw_tenth(self, value, pos, text, textures):

        self.draw_surface_screen(textures.clock_2[value], pos, True, on_this_surface=text)
        pos[0] = pos[0] + 15

        return text, pos

    def big_log(self, text, textures):

        if text is not None:

            rend_text = textures.font["default"].render(text, True, textures.colors["button text"])
            self.draw_surface_screen(rend_text, (c.X_MID, c.Y_SIZE / 26))

    def set_caption(self, caption=c.GAME_NAME):
        """
        set the window caption
        """
        self.caption = caption
        pygame.display.set_caption(caption)


