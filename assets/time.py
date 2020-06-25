# -*- coding: utf-8 -*-

"""
Related to time or the clock
"""

import pygame
import assets.consts as c
from assets.display import Display
import assets.settings as s


class Time:
    """
    time
    """
    def __init__(self):

        self.clock = pygame.time.Clock()

    def tick(self):
        """
        limit frame rate
        """
        self.clock.tick(c.FPS)


class Clock(Time, Display):
    """
    in game clock_bol
    """
    def __init__(self, settings):

        Display.__init__(self)

        self.stopwatch = pygame.time

        self.clock_bol = True  # allow clock_bol

        self.last_update = None

        self.update_clock_bol = False

        self.last_infos = None

        self.table = pygame.Surface(c.TB_SIZE, pygame.SRCALPHA, 32)

        if self.clock_bol:
            # list that stores clock_bol data in the form [white, black]

            # total time used by the player each round
            self.player_stopwatch = [0, 0]
            # beginning of the time measurement
            self.last_check = [0, 0]
            # end of the time measurement
            self.check = [0, 0]

            # clock_bol value at the beginning in milliseconds and during all the game
            self.last_player_clock = settings.game['clock'][0]
            self.player_clock = list(self.last_player_clock)

        # value in milliseconds of the incrementation (0 = no incrementation)
        self.clock_incrementation = settings.game['clock'][1]

    def start_clock(self, game):
        """
        start the clock_bol of the player
        """
        self.last_check[game.turn_number % 2] = self.stopwatch.get_ticks()
        self.last_update = self.stopwatch.get_ticks()

    def update_clock_value(self, game):
        """
        update the clock value
        """
        if self.clock_bol:
            i = game.turn_number % 2

            self.player_stopwatch[i] = self.stopwatch.get_ticks() - self.last_check[i]

            self.player_clock[i] = self.player_clock[i] - self.player_stopwatch[i]

            self.last_check[(game.turn_number + 1) % 2] = self.stopwatch.get_ticks()

            self.last_check[i] = self.stopwatch.get_ticks()

            # check if the timer on screen needs to be updated
            for i, _ in enumerate(self.last_player_clock):
                if self.last_player_clock[i]//100 != self.player_clock[i]//100 or self.last_infos != (game.turn, game.process):
                    self.last_infos = (game.turn, game.process)
                    self.last_player_clock = self.player_clock.copy()
                    self.update_clock_bol = True

                # if time is negative : end the game and lock the time to 0 for the one who ran out of time
                if self.player_clock[i] < 0:
                    game.log = game.turn, "{} lost ! Run out of time".format(game.turn.capitalize())
                    self.player_clock[i] = 0
                    game.stop()

    def stop_clock(self):
        """
        block the clocks
        """
        self.clock_bol = False

    def draw_table(self, game, textures):
        """
        draw the full table on the right of the screen
        """

        table = self.draw_states(game.turn, game.process, textures)

        your_turn = True

        for i in [c.TURN_STATE[game.turn],  c.TURN_STATE[game.last_turn]]:

            clock_surface = self.draw_clock(clock_timer=self.player_clock[i], turn=your_turn, textures=textures)
            self.draw_surface(draw_this_surface=clock_surface, disp_pos=c.CLOCK[i], on_this_surface=table, center=True)
            your_turn = False

        self.table = table

    def draw_states(self, turn, state, textures):
        """
        on the table draw the states
        """

        table = pygame.Surface(c.TB_SIZE, pygame.SRCALPHA, 32)
        table.fill(textures.colors["infos"])

        self.draw_surface(draw_this_surface=textures.write(turn), disp_pos=c.TURN_P, center=True, on_this_surface=table)
        self.draw_surface(draw_this_surface=textures.write(state, font="game infos"), disp_pos=c.PROCESS_P, center=True,
                          on_this_surface=table)

        return table

    @staticmethod
    def calc_time(clock_timer):
        seconds = clock_timer // 1000
        minutes = seconds // 60
        hours = minutes // 60

        minutes = minutes - 60 * hours
        seconds = seconds - 60 * minutes - 60 ** 2 * hours
        tenth = "{:03d}".format(clock_timer)[-3]

        return hours, minutes, seconds, tenth

    def draw_clock(self, clock_timer, turn, textures):

        stopwatch = pygame.Surface((200, 60), pygame.SRCALPHA, 32)

        if turn:
            stopwatch.fill(textures.colors["clock turn"])

        else:
            stopwatch.fill(textures.colors["clock not turn"])

        text = pygame.Surface((200, 60), pygame.SRCALPHA, 32)

        hours, minutes, seconds, tenth = self.calc_time(clock_timer)

        # hours
        if hours > 0:
            if hours < 10:
                pos = [20, 30]
                text, pos = self.draw_1_chr(hours, pos, text, textures)
                text, pos = self.draw_small_chr(":", pos, text, textures)
                text, pos = self.draw_2_chr(minutes, pos, text, textures)
                text, pos = self.draw_small_chr(".", pos, text, textures)
                text, pos = self.draw_small_2_chr(seconds, pos, text, textures)

            else:
                pos = [20, 30]
                text, pos = self.draw_2_chr(hours, pos, text, textures)
                text, pos = self.draw_small_chr(":", pos, text, textures)
                text, pos = self.draw_2_chr(minutes, pos, text, textures)
                text, pos = self.draw_small_chr(".", pos, text, textures)
                text, pos = self.draw_tenth(str(seconds // 10), pos, text, textures)

        elif minutes > 1:
            pos = [46, 30]
            text, pos = self.draw_2_chr(minutes, pos, text, textures)
            text, pos = self.draw_small_chr(":", pos, text, textures)
            text, pos = self.draw_2_chr(seconds, pos, text, textures)


        else:
            pos = [22, 30]
            text, pos = self.draw_2_chr(minutes, pos, text, textures)
            text, pos = self.draw_small_chr(":", pos, text, textures)
            text, pos = self.draw_2_chr(seconds, pos, text, textures)
            text, pos = self.draw_small_chr(".", pos, text, textures)
            text, pos = self.draw_tenth(tenth, pos, text, textures)

        pos = stopwatch.get_rect().center

        self.draw_surface(draw_this_surface=text, disp_pos=pos, center=True, on_this_surface=stopwatch)

        return stopwatch

    def draw_2_chr(self, value, pos, text, textures):
        temp = "{:02d}".format(value)
        for char in temp:
            self.draw_surface(draw_this_surface=textures.clock_1[char], disp_pos=pos, center=True, on_this_surface=text)
            pos[0] = pos[0] + 26

        return text, pos

    def draw_1_chr(self, value, pos, text, textures):
        temp = "{:01d}".format(value)
        for char in temp:
            self.draw_surface(draw_this_surface=textures.clock_1[char], disp_pos=pos, center=True, on_this_surface=text)
            pos[0] = pos[0] + 28

        return text, pos

    def draw_small_chr(self, value, pos, text, textures):
        self.draw_surface(draw_this_surface=textures.clock_1[value], disp_pos=pos, center=True, on_this_surface=text)
        pos[0] = pos[0] + 20

        return text, pos

    def draw_small_2_chr(self, value, pos, text, textures):
        temp = '{:02d}'.format(value)
        for char in temp:
            self.draw_surface(draw_this_surface=textures.clock_2[char], disp_pos=pos, center=True, on_this_surface=text)
            pos[0] = pos[0] + 22

        return text, pos

    def draw_tenth(self, value, pos, text, textures):
        self.draw_surface(draw_this_surface=textures.clock_2[value], disp_pos=pos, center=True, on_this_surface=text)
        pos[0] = pos[0] + 22

        return text, pos
