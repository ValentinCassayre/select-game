# -*- coding: utf-8 -*-

"""
Settings
"""
import pickle

import assets.consts as c


class Settings:
    """
    settings
    """
    def __init__(self):
        self.game = {}
        self.new()

    def value(self, name, n=2):
        if n < 0:
            return c.MENU_VARIABLES[name][self.game[name]]
        else:
            return c.MENU_VARIABLES[name][self.game[name]][n]

    def new(self):
        for name in c.MENU_VARIABLES:
            self.game[name] = 0

    def save(self):
        """
        save current object
        """
        file = open('settings', 'wb')
        obj = self.game
        pickle.dump(obj, file)
        file.close()

    def load(self):
        """
        load settings
        """
        file = open('settings', 'rb')
        self.game = pickle.load(file)
        file.close()
