"""
check events (mouse, keyboard, leave etc)
"""

import pygame


class Events:

    def __init__(self):
        pass

    @staticmethod
    def check(mask_list=[]):

        event_key = None
        mask_touching = []
        click = False

        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type is pygame.QUIT:
                event_key = "leave"

            elif event.type is pygame.KEYDOWN:

                if event.key is pygame.K_ESCAPE:
                    event_key = "escape"

                if event.key is pygame.K_SPACE:
                    event_key = "space"

                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    event_key = "return"

            for mask in mask_list:
                # tile[n] : 0 rect 1 mask 2 disp pos 3 type 4 optional if board : board pos
                pos_in_mask = x - mask[0].x, y - mask[0].y
                touching = mask[0].collidepoint(*(x, y)) and mask[1].get_at(pos_in_mask)

                if touching:
                    mask_touching.append(mask)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # tile clicked
                        click = True

        return event_key, mask_touching, click
