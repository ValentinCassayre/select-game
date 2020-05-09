"""
Textures of the game
"""

import pygame
from pygame import gfxdraw
from os import path
from math import cos, sin, pi

import assets.consts as c


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

        for name in ["menu_title", "menu_sub_1", "button", "button_overlay", "bg_hex"]:
            self.dflt[name] = self.create_dflt(name)

        for name in ["tile_1", "tile_2", "tile_overview", "tile_select", "tile_mask", "tile_way", "tile_eat",
                     "tile_setback", "tile_move"]:
            self.game[name] = self.create_game(name)

        for name in ["takeback", "offer_draw", "give_up"]:
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
            with open(c.COLORS_DFLT, "r") as colors:
                for line in colors:
                    if line.startswith("# ") or line.startswith("\n"):
                        continue
                    else:
                        line = line.replace("\n", "").split()
                        name = line[0]
                        color = tuple(map(int, line[2].split(",")))
                        self.colors.update({name: color})
                        self.insect_path = c.INSECTS
                colors.close()
        except NameError:
            with open("default textures/colors.txt", "r") as colors:
                for line in colors:
                    if line.startswith("# ") or line.startswith("\n"):
                        continue
                    else:
                        line = line.replace("\n", "").split()
                        name = line[0]
                        color = tuple(map(int, line[2].split(",")))
                        self.colors.update({name: color})
                        self.insect_path = c.INSECTS
                colors.close()

    def create_dflt(self, name):

        image = None

        if name.startswith("menu"):
            if name.endswith("title"):
                image = self.font["menu title"].render(c.GAME_NAME, True, self.colors["tile_2"])
            elif name.endswith("sub_1"):
                image = self.font["menu sub 1"].render(c.SUB1, True, self.colors["tile_1"])

        if name == "button":
            image = self.draw_tile(self.colors["button"], radius=c.MENU_RADIUS, unit=c.MENU_UNIT*2, mult=1)

        if name == "button_overlay":
            image = self.draw_tile(self.colors["button_overview"], radius=c.MENU_RADIUS, unit=c.MENU_UNIT*2, mult=1)

        if name == "bg_hex":
            image = self.draw_tile(self.colors["background_2"], radius=c.MENU_RADIUS, unit=c.MENU_UNIT*2, mult=1)

        if image is not None:
            pygame.image.save(image, c.SCREENSHOTS + name + ".png")
            return image

    def create_game(self, name):

        image = None

        try:
            image = self.draw_tile(self.colors[name]).convert_alpha()

        except KeyError:
            if name == "tile_mask":
                image = self.draw_tile(c.BLACK).convert_alpha()

        if image is not None:
            pygame.image.save(image, c.SCREENSHOTS + name + ".png")
            return image

    def create_game_but(self, name):

        try:
            image = pygame.image.load("textures/buttons" + name + ".png")
        except pygame.error:
            image = pygame.image.load("assets/default textures/buttons/" + name + ".png")

        return image

    def create_digit(self, digit, size):

        image = self.font["clock_{}".format(size)].render(digit, True, self.colors["text"])

        return image

    def stopwatch(self, time):

        image = self.font["clock_1"].render(time, True, self.colors["text"])

        return image

    def save_board(self, board):
        self.game["board"] = board.convert_alpha()
        pygame.image.save(board, c.SCREENSHOTS + "/board.png")

    def save_insect(self, insect_full_name, insect):
        self.dflt[insect_full_name] = insect.convert_alpha()

    def draw_hexagon(self, image, color_in, rect, radius=c.RADIUS, mult=1.0, fill=True):
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

    def draw_tile(self, color, radius=c.RADIUS, unit=c.UNIT*2, mult=1.0, fill=True, alpha=32):
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
        rect = pygame.Rect((0, 0), (2 * c.RADIUS * mult, c.UNIT * 2 * mult))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image = self.draw_hexagon(image, self.colors["COLOR_TILE_OUTLINE"], rect, c.RADIUS, mult)
        image = self.draw_hexagon(image, color, rect, c.RADIUS)
        return image

    @staticmethod
    def coords(pos, radius=c.RADIUS, mult=1.0):
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

        fonts["clock_1"] = pygame.font.Font(font_path, round(font_size * 2.4))
        fonts["clock_2"] = pygame.font.Font(font_path, round(font_size * 2))

        fonts["game infos"] = pygame.font.Font(font_path, round(font_size * 1.6))

        return fonts
