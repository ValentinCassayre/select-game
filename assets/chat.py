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
        self.input_value = ''
        self.table = None
        self.player_name = 'Definity_'

        self.selected = False
        self.input = False

        self.chat_input_box = pygame.Surface(c.TB_SIZE, pygame.SRCALPHA, 32)
        self.chat_input_box.fill((130, 130, 130))

        self.chat_input_button = [self.convert_to_mask(self.chat_input_box, c.TBL, "chat")]

    def add_message(self, message, decorator=''):
        self.update_chat_bol = True

        if message == '' or message == ' ':
            return

        else:
            self.messages.append(message)

            max_len = 24-len(decorator)
            self.formatted_messages.append(decorator + message[0:max_len])
            message = message[max_len:256]

            while message != '':
                self.formatted_messages.append(message[0:24])
                message = message[24:-1]

    def add_input_value(self, message):
        self.update_chat_bol = True
        self.input_value = message

    def update(self, textures):
        self.table = pygame.Surface(c.TB_SIZE, pygame.SRCALPHA, 32)
        self.table.fill(textures.colors["infos"])

        messages = self.formatted_messages.copy()
        messages.reverse()
        pos = list(c.CHAT_POS)

        self.draw_surface(draw_this_surface=self.chat_input_box, disp_pos=(0, c.TB_SIZE[1]-c.CHAT_FONT_SIZE),
                          center=False, on_this_surface=self.table)

        if self.input:

            self.draw_surface(draw_this_surface=textures.write(self.input_value[-24:]+'|', font='chat'),
                              disp_pos=(10, c.TB_SIZE[1] - c.CHAT_FONT_SIZE), center=False, on_this_surface=self.table)

        for message in messages:
            self.draw_surface(draw_this_surface=textures.write(message, font='chat'), disp_pos=pos, center=False,
                              on_this_surface=self.table)

            pos[1] -= c.CHAT_FONT_SIZE

        self.draw_surface(draw_this_surface=textures.write('Chat'), disp_pos=c.CENTER, center=False,
                          on_this_surface=self.table)
