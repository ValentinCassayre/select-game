"""
Textures of the game
"""

import pygame
from pygame import gfxdraw
from os import path

from math import cos, sin, pi

from assets.math import Math as M
import assets.consts as c
from assets.display import Display as D


class Textures:
    """
    creates all the textures needed
    textures are in pygame surface format
    """

    def __init__(self):

        # import colors
        self.colors = {}
        self.insect_path = None
        self.import_colors()

        self.font = self.create_font()

        self.game = {}
        self.dflt = {}

        self.clock_1 = {}
        self.clock_2 = {}

        self.game_but = {}

        for name in ["menu title", "menu sub 1", "button", "button overlay", "bg hex"]:
            self.dflt[name] = self.create_dflt(name)

        for name in ["tile 1", "tile 2", "tile overview", "tile select", "tile mask", "tile way", "tile eat",
                     "tile setback", "tile move"]:
            self.game[name] = self.create_game(name)

        for name in ["takeback", "offer takeback", "accept takeback",
                     "draw", "offer draw", "accept draw",
                     "resign",
                     "play again",
                     "menu"]:
            self.game_but[name] = self.create_game_but(name)

        for digit in range(10):
            digit = str(digit)
            self.clock_1[digit] = self.create_digit(digit, 1)
            self.clock_2[digit] = self.create_digit(digit, 2)
        for stopwatch_car in [":", ",", "."]:
            self.clock_1[stopwatch_car] = self.create_digit(stopwatch_car, 1)
            self.clock_2[stopwatch_car] = self.create_digit(stopwatch_car, 2)

    def import_colors(self):
        """
        import the colors from the "colors.txt" file
        """
        try:
            self.open_file('assets/default textures/colors.txt')
        except FileNotFoundError:
            self.open_file('default textures/colors.txt')

    def open_file(self, file):
        """
        open and convert colors file
        """
        with open(file, 'r') as colors:
            for line in colors:
                if line.startswith('# ') or line.startswith('\n'):
                    continue
                else:
                    color_dat = self.format_text(line).split('=')
                    name = color_dat[0]
                    color = tuple(map(int, color_dat[1].split(',')))
                    self.colors.update({name: color})
                    self.insect_path = c.INSECTS
            colors.close()

    def create_dflt(self, name):

        image = None

        if name.startswith("menu"):
            if name.endswith("title"):
                image = self.font["menu title"].render(c.GAME_NAME, True, self.colors["tile 2"])
            elif name.endswith("sub 1"):
                image = self.font["menu sub 1"].render(c.SUB1, True, self.colors["tile 1"])

        if name == "button":
            image = self.draw_tile(self.colors["button"], radius=c.MENU_RADIUS, unit=c.MENU_UNIT*2, mult=1)

        if name == "button overlay":
            image = self.draw_tile(self.colors["button overview"], radius=c.MENU_RADIUS, unit=c.MENU_UNIT*2, mult=1)

        if name == "bg hex":
            image = self.draw_tile(self.colors["background 2"], radius=c.MENU_RADIUS, unit=c.MENU_UNIT*2, mult=1)

        if image is not None:
            pygame.image.save(image, c.SCREENSHOTS + name + ".png")
            return image

    def create_game(self, name):

        image = None

        try:
            image = self.draw_tile(self.colors[name]).convert_alpha()

        except KeyError:
            if name == "tile mask":
                image = self.draw_tile(c.BLACK).convert_alpha()

        if image is not None:
            pygame.image.save(image, c.SCREENSHOTS + name + ".png")
            return image

    def create_game_but(self, name):

        radius = 80
        mult = 1
        unit = M.inscribed_rad(radius)

        rect = pygame.Rect((0, 0), (2 * radius * mult, unit * mult))
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32)

        image = self.draw_hexagon(image, self.colors['game buttons'], rect, radius, mult)

        value = name.capitalize()
        if len(name) < 14:
            text_format = 'game menu 1'
        else:
            text_format = 'game menu 2'

        text = self.font[text_format].render(value, True, self.colors['game buttons text'])

        D.draw_surface(text, image, middle=True)

        pygame.image.save(image, c.SCREENSHOTS + name + ".png")

        return image

    def create_digit(self, digit, size):

        image = self.font["clock {}".format(size)].render(digit, True, self.colors["text"])

        return image

    def stopwatch(self, time):

        image = self.font["clock 1"].render(time, True, self.colors["text"])

        return image

    def save_board(self, board):
        self.game["board"] = board.convert_alpha()
        pygame.image.save(board, c.SCREENSHOTS + "/board.png")

    def save_insect(self, insect_full_name, insect):
        image = pygame.image.load(insect.path + insect.full_name + ".png")
        self.dflt[insect_full_name] = image.convert_alpha()

    def draw_hexagon(self, image, color_in, rect, radius=c.R, mult=1.0, fill=True):
        """
        return a surface with the shape of an hexagon
        """
        # create a surface of the selected area (pygame.SRCALPHA = include alpha pixel flag)
        temp = pygame.Surface(rect.size, pygame.SRCALPHA, 32)

        # draw the hexagon using gfxdraw for antialiased (smooth) -> NOT WORKING WELL SO NO !
        # i let this for the moment
        # usefull : .draw.aaline aalines or .gfxdraw.aapolygon
        # WARNING AALINE ONLY DRAW IF NOT HORIZONTAL OR VERTICAL !
        # for the moment :
        if fill:
            pygame.draw.polygon(temp, color_in, self.coords(rect.center, radius, mult))
        else:
            pygame.gfxdraw.polygon(temp, self.coords(rect.center, radius, mult), color_in)

        # blit the surface to the top left edge
        image.blit(temp, rect.topleft)
        return image.convert_alpha()

    def draw_tile(self, color, radius=c.R, unit=c.U * 2, mult=1.0, fill=True, alpha=32):
        """
        inner tile pnly
        """
        # create a selection of the area
        rect = pygame.Rect((0, 0), (2 * radius * mult, unit * mult))
        image = pygame.Surface(rect.size, pygame.SRCALPHA, alpha)

        image = self.draw_hexagon(image, color, rect, radius, mult, fill)

        return image

    def draw_tile_board(self, color, mult=1.2):
        """
        special tile for the board
        """
        # create a selection of the area
        rect = pygame.Rect((0, 0), (2 * c.R * mult, c.U * 2 * mult))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image = self.draw_hexagon(image, self.colors["COLOR TILE OUTLINE"], rect, c.R, mult)
        image = self.draw_hexagon(image, color, rect, c.R)
        return image

    @staticmethod
    def coords(pos, radius=c.R, mult=1.0):
        """
        create the coordinates of the 6 points of the hexagon calculated with the pi/3 modulo
        pos is a tuple of the coordinates on the screen and not on the board
        to convert position from board to screen use position()
        :return: list of coords (tuples)
        """
        x, y = pos
        coords = []
        for k in range(6):
            coords.append((x + mult * radius * cos(k * pi / 3),
                           y + mult * radius * sin(k * pi / 3)))
        return coords

    @staticmethod
    def draw_insect(path_str):
        """
        Draw the insects
        """
        # load pygame and convert alpha
        image = pygame.image.load(path_str).convert_alpha()
        return image

    def write(self, text, font="default"):

        text = self.font[font].render(text, True, self.colors["text"])

        return text

    @staticmethod
    def create_font():
        fonts = {}
        font_path = path.join(c.FONTS, "mysteron.ttf")
        font_size = 20

        fonts["default"] = pygame.font.Font(font_path, round(font_size * 2))

        fonts["menu title"] = pygame.font.Font(font_path, round(font_size * 6))
        fonts["menu sub 1"] = pygame.font.Font(font_path, round(font_size * 1.5))
        fonts["menu button"] = pygame.font.Font(font_path, round(font_size * 1.6))
        fonts["menu button sub"] = pygame.font.Font(font_path, round(font_size * 1.2))

        fonts["clock 1"] = pygame.font.Font(font_path, round(font_size * 2.4))
        fonts["clock 2"] = pygame.font.Font(font_path, round(font_size * 2))

        fonts["game infos"] = pygame.font.Font(font_path, round(font_size * 1.6))

        fonts["game menu 1"] = pygame.font.Font(font_path, round(font_size))
        fonts["game menu 2"] = pygame.font.Font(font_path, round(font_size*0.8))

        return fonts

    @staticmethod
    def format_text(text):
        """
        predefined format text convertor
        """
        text = Textures.replace_all(text, {'\n': '', ' ': '', '_': ' '})
        return text

    @staticmethod
    def replace_all(text, substrings_dict):
        """
        replace multiple substrings into a string
        """
        for old in substrings_dict:
            new = substrings_dict[old]
            text = text.replace(old, new)
        return text
