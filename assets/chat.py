# -*- coding: utf-8 -*-

"""
Related to the left chat box
"""

import pygame
import assets.consts as c
from assets.display import Display


class ChatBox(Display):
    """
    in game clock_bol
    """
    def __init__(self):

        Display.__init__(self)
        self.update_chat_bol = True
        self.pos = [10, c.TB_SIZE[1]]
        self.messages = []
        self.formatted_messages = []
        self.table = None
        self.player_name = 'Definity_'

    def add_message(self, message):
        self.update_chat_bol = True
        self.messages.append(message)

        if message.startswith('/'):
            pass
        else:
            decorator = '{} : '.format(self.player_name)
            self.formatted_messages.append(decorator + message[0:24-len(decorator)])
            message = message[24-len(decorator):256]

            while message != '':
                self.formatted_messages.append(message[0:24])
                message = message[24:-1]

    def update(self, textures):
        table = pygame.Surface(c.TB_SIZE, pygame.SRCALPHA, 32)
        table.fill(textures.colors["infos"])

        messages = self.formatted_messages.copy()
        messages.reverse()
        pos = list(c.CHAT_POS)
        for message in messages:
            self.draw_surface(draw_this_surface=textures.write(message, font='chat'), disp_pos=pos, center=False,
                              on_this_surface=table)

            pos[1] -= c.CHAT_FONT_SIZE

        self.draw_surface(draw_this_surface=textures.write('Chat'), disp_pos=c.CENTER, center=False,
                          on_this_surface=table)

        self.table = table
