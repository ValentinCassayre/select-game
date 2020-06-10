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

        # Keyboard related

        self.key = None

        # Masks related

        self.mask_touching = []

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

        for event in pygame.event.get():

            self.mouse_pos = (x, y)

            if event.type is pygame.QUIT:
                self.key = "leave"

            elif event.type is pygame.KEYDOWN:

                if event.key is pygame.K_ESCAPE:
                    self.key = "escape"

                if event.key is pygame.K_SPACE:
                    self.key = "space"

                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    self.key = "return"

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
