# -*- coding: utf-8 -*-

"""
check events (mouse, keyboard, leave etc)
"""

import pygame


class Events:

    def __init__(self):
        """
        initialize default states
        """

        # Mouse related

        self.click = False
        self.mouse_pos = None
        self.mouse_but_down = False
        self.move = False

        # Keyboard related

        self.key = None
        self.input_value = ''
        self.message = None

        # Masks related

        self.mask_touching = []

        # Other

        self.main_loop = True
        self._state = 'menu main'
        self.last_state = 'leave'

        # Game related

        self.drag = False
        self.selected_insect = None
        self.disp_drag = False
        self.initial_pos = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self.last_state = self._state
        self._state = state

    def check(self, mask_list=None):
        """
        check all the events
        """

        if mask_list is None:
            mask_list = []

        self.key = None
        self.mask_touching = []
        self.click = False

        x, y = pygame.mouse.get_pos()

        # check if mouse moved
        if self.mouse_pos == (x, y):
            self.move = False
        else:
            self.move = True

        # update mouse position
        self.mouse_pos = (x, y)

        for event in pygame.event.get():

            if event.type is pygame.QUIT:
                self.main_loop = False

            elif event.type is pygame.KEYDOWN:

                if event.key is pygame.K_ESCAPE:
                    self.key = "escape"

                if event.key is pygame.K_SPACE:
                    self.key = "space"

                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    self.key = "return"
                    self.message = self.input_value
                    self.input_value = ''

                elif event.key == pygame.K_BACKSPACE:
                    self.input_value = self.input_value[:-1]
                else:
                    self.input_value += event.unicode

            for mask in mask_list:

                # tile[n] : 0 rect 1 mask 2 disp pos 3 type 4 optional if board : board pos
                pos_in_mask = x - mask[0].x, y - mask[0].y
                touching = mask[0].collidepoint(*(x, y)) and mask[1].get_at(pos_in_mask)

                if touching:
                    self.mask_touching.append(mask)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # tile clicked
                self.click = True
                self.mouse_but_down = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_but_down = False

    def game_check(self, game):
        """
        prototype
        check specific events for a game
        """

        if self.click:
            self.initial_pos = self.mouse_pos
            game.update_process = True

        if self.mouse_but_down:
            self.drag = True
            if not self.disp_drag:
                if self.move:
                    self.disp_drag = True

        else:
            if self.drag is True:
                self.drag = False
                game.update_process = True
            self.disp_drag = False
            self.initial_pos = None

        game.drag = self.drag
        game.disp_drag = self.disp_drag
        game.initial_pos = self.initial_pos

