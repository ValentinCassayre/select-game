# -*- coding: utf-8 -*-

"""
Menu
"""

import pygame
import assets.consts as c
from assets.display import Display
from webbrowser import open as open_url


class Menu(Display):
    """
    Class about each menus of the game
    """

    def __init__(self):
        """
        Constructor
        """
        Display.__init__(self)

        self.menus = {}

        self.text_menu = {
            'infos': {(0, 0): ('state/last', 'Back', 'To the menu'),
                      (0, 1): ('browse/github', 'Git Hub', 'Webpage'),
                      (1, 0): ('browse/website', 'Website', 'In french'),
                      (1, 1): ('leave', 'Quit game', '')},
            'main': {(0, 0): ('state/game', 'Two players', 'Offline'),
                     (0, 1): ('state/tutorial', 'Tutorial', 'Soon'),
                     (1, 0): ('state/menu infos', 'More infos', 'Links'),
                     (1, 1): ('state/game', 'Computer', 'Offline')},
            'pause': {(0, 0): ('state/last', 'Resume', ''),
                      (0, 1): ('save', 'Save', 'Soon'),
                      (1, 0): ('browse/github', 'Git Hub', 'Webpage'),
                      (1, 1): ('leave', 'Quit', 'Save')}
        }

        self.button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.last_touched_mask = None
        self.update_display = False

    def load(self, textures):
        """
        create all the structures of the menus
        """

        for menu in self.text_menu:
            self.menus[menu] = self.create_menu(self.text_menu[menu], textures)

    def create_menu(self, data, textures):
        """
        method used to create a menu using
        """

        menu_but_masks = []

        text_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        bg = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        for i in range(-3, 4):
            for j in range(-3, 4):

                pos = (i, j)

                x = c.X_MID + (i * 3 * c.MENU_RADIUS / 2 - j * 3 * c.MENU_RADIUS / 2) * c.MENU_EDGE
                y = c.Y_MID + (i * c.MENU_UNIT + j * c.MENU_UNIT) * c.MENU_EDGE

                if pos in data:

                    self.draw_surface(draw_this_surface=textures.dflt["button"], on_this_surface=bg, disp_pos=(x, y))

                    text = \
                        textures.font["menu button"].render(data[pos][1], True, textures.colors["button text"])

                    self.draw_surface(draw_this_surface=text, on_this_surface=text_surface, disp_pos=(x, y))

                    text = \
                        textures.font["menu button sub"].render(data[pos][2], True, textures.colors["button text sub"])

                    self.draw_surface(draw_this_surface=text, on_this_surface=text_surface, disp_pos=(x, y + 30))

                    menu_but_masks.append(self.convert_to_mask(textures.dflt["button"], (x, y), data[pos][0]))

                else:
                    self.draw_surface(draw_this_surface=textures.dflt["bg hex"], disp_pos=(x, y), on_this_surface=bg)

        self.draw_surface(draw_this_surface=textures.dflt["menu title"], disp_pos=c.TITLE_POS, on_this_surface=text_surface, center=True)
        self.draw_surface(draw_this_surface=textures.dflt["menu sub 1"], disp_pos=c.SUB1_POS, on_this_surface=text_surface, center=True)

        # bg is the background, text_surface is the text overlay surface, menu_but_masks are the masks used for button
        return bg, text_surface, menu_but_masks

    def init(self, menu_name):
        """
        before going in the loop
        """
        self.update_display = True
        self.last_touched_mask = None
        self.set_caption('{} - {} menu'.format(c.GAME_NAME, menu_name.capitalize()))

    def update(self, menu, events, textures):
        """
        update display using events
        """

        # check events
        events.check(mask_list=self.menus[menu][2])

        if events.key is 'escape':
            if events.state == 'menu main':
                events.main_loop = False
            else:
                events.state = 'menu main'

        if events.key in ["space", "enter"]:
            if events.state == 'menu pause':
                events.state = events.last_state

        for touched_mask in events.mask_touching:

            if events.click:

                key = touched_mask[3].split('/')

                if key[0] == 'leave':
                    events.main_loop = False

                elif key[0] == 'state':
                    if key[1] == 'last':
                        events.state = events.last_state
                    else:
                        events.state = key[1]

                elif key[0] == 'browse':
                    open_url(c.url[key[1]])

            elif self.last_touched_mask is not touched_mask[3]:

                self.button = self.draw_surface(draw_this_surface=textures.dflt["button overlay"],
                                                disp_pos=touched_mask[2], on_this_surface=self.button, center=True)
                self.update_display = True
                self.last_touched_mask = touched_mask[3]

        if self.update_display:
            # clean screen
            self.draw_screen()
            # draw new menu
            self.draw_surfaces(surface_list=[self.menus[menu][0], self.button, self.menus[menu][1]])
            # update screen
            pygame.display.flip()
            # clean buttons surface
            self.button = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
            # reset
            self.update_display = False
