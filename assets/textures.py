"""
Stuff for displaying stuff
"""

from pygame import gfxdraw
import os

from assets.consts import *
from assets.display import *
from assets.insects import *


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
        for name in ["menu_title", "menu_sub_1", "menu_sub_2", "button", "button_overlay", "bg_hex"]:
            self.dflt[name] = self.create_dflt(name)

        for name in ["tile_1", "tile_2", "tile_overview", "tile_select", "tile_mask", "tile_way", "tile_eat"]:
            self.game[name] = self.create_game(name)

    def import_colors(self):
        """
        import the colors from the "colors.txt" file
        """
        try:
            with open("assets/textures/colors.txt", "r") as colors:
                for line in colors:
                    if line.startswith("# ") or line.startswith("\n"):
                        continue
                    else:
                        line = line.replace("\n", "").split()
                        name = line[0]
                        color = tuple(map(int, line[2].split(",")))
                        self.colors.update({name: color})
                        self.insect_path = 'assets/textures/insects/'
                colors.close()
        except:
            with open("assets/default textures/colors.txt", "r") as colors:
                for line in colors:
                    if line.startswith("# ") or line.startswith("\n"):
                        continue
                    else:
                        line = line.replace("\n", "").split()
                        name = line[0]
                        color = tuple(map(int, line[2].split(",")))
                        self.colors.update({name: color})
                        self.insect_path = 'assets/default textures/insects/'
                colors.close()

    def create_dflt(self, name):

        image = None

        if name.startswith("menu"):
            if name.endswith("title"):
                image = self.font["menu title"].render(GAME_NAME, True, self.colors["COLOR_TILE_2"])
            elif name.endswith("sub_1"):
                image = self.font["menu sub 1"].render(SUB1, True, self.colors["COLOR_TILE_1"])
            elif name.endswith("sub_2"):
                image = self.font["menu sub 2"].render(SUB2, True, self.colors["COLOR_TEXT_1"])

        if name == "button":
            image = self.draw_tile(self.colors["BUTTON"], radius=128, unit=math.sqrt(5)*128/2, mult=1)

        if name == "button_overlay":
            image = self.draw_tile(self.colors["COLOR_TILE_OVERVIEW"], radius=128, unit=math.sqrt(5)*128/2, mult=1)

        if name == "bg_hex":
            image = self.draw_tile(self.colors["BG2"], radius=128, unit=math.sqrt(5) * 128 / 2, mult=1)

        if image is not None:
            pygame.image.save(image, "assets/screenshots/" + name + ".png")
            return image

    def create_game(self, name):

        image = None

        if name.endswith("1"):
            image = self.draw_tile(self.colors["COLOR_TILE_1"]).convert_alpha()
        elif name.endswith("2"):
            image = self.draw_tile(self.colors["COLOR_TILE_2"]).convert_alpha()
        elif name.endswith("overview"):
            image = self.draw_tile(self.colors["COLOR_TILE_OVERVIEW"]).convert_alpha()
        elif name.endswith("select"):
            image = self.draw_tile(self.colors["COLOR_TILE_SELECT"]).convert_alpha()
        elif name.endswith("way"):
            image = self.draw_tile(self.colors["COLOR_TILE_WAY"]).convert_alpha()
        elif name.endswith("eat"):
            image = self.draw_tile(self.colors["COLOR_TILE_EAT"]).convert_alpha()
        elif name.endswith("mask"):
            image = self.draw_tile(BLACK).convert_alpha()

        if image is not None:
            pygame.image.save(image, "assets/screenshots/" + name + ".png")
            return image


    def save_board(self, board):
        self.game["board"] = board.convert_alpha()
        pygame.image.save(board, "assets/screenshots/board.png")

    def save_insect(self, insect_full_name, insect):
        self.dflt[insect_full_name] = insect.convert_alpha()

    def coords(self, pos, radius=RADIUS, mult=1.0):
        """
        create the coordinates of the 6 points of the hexagon calculated with the pi/3 modulo
        pos is a tuple of the coordinates on the screen and not on the board
        to convert position from board to screen use position()
        :return: list of coords (tuples)
        """
        x, y = pos
        coords = []
        for k in range(6):
            coords.append((x + mult * radius * math.cos(k * math.pi / 3),
                           y + mult * radius * math.sin(k * math.pi / 3)))
        return coords

    def draw_hexagon(self, image, color_in, rect, radius=RADIUS, mult=1.0, fill=True):
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

    def draw_tile(self, color, radius=RADIUS, unit=UNIT, mult=1.0, fill=True, alpha=32):
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
        rect = pygame.Rect((0, 0), (2 * RADIUS * mult, UNIT * mult))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image = self.draw_hexagon(image, self.colors["COLOR_TILE_OUTLINE"], rect, RADIUS, mult)
        image = self.draw_hexagon(image, color, rect, RADIUS)
        return image

    @staticmethod
    def draw_insect(path, radius=RADIUS, unit=UNIT):
        """
        Draw the insects
        """
        # create a selection of the area
        rect = pygame.Rect((0, 0), (2 * radius, unit))

        # if image is drawn
        image = pygame.Surface(rect.size, pygame.SRCALPHA)

        # if image come from an png
        image = pygame.image.load(path).convert_alpha()
        return image

    @staticmethod
    def create_font():
        fonts = {}
        font_path = os.path.join("assets/fonts", "mysteron.ttf")
        font_size = 20
        fonts["menu title"] = pygame.font.Font(font_path, round(font_size * 6))
        fonts["menu sub 1"] = pygame.font.Font(font_path, round(font_size * 2))
        fonts["menu sub 2"] = pygame.font.Font(font_path, round(font_size * 1.6))
        return fonts
