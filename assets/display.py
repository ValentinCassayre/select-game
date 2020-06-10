"""
Display
"""

import pygame
import assets.consts as c


class Display:
    """
    display mother class : everything related to things on the screen
    """
    def __init__(self):
        """
        Constructor
        """
        # name the window
        pygame.display.set_caption(c.GAME_NAME)
        # add an icon
        pygame.display.set_icon(pygame.image.load(c.ICON))
        # Create a python surface for the screen
        self.screen = pygame.display.set_mode(c.SCREEN_SIZE)

        self.stopwatch = pygame.Surface((200, 60), pygame.SRCALPHA, 32)

    # basic tools
    def draw_screen(self):
        """
        Create white background on the screen
        """
        self.screen.fill(c.BACKGROUND_COLOR)

    def draw_surface_screen(self, draw_this_surface, disp_pos, center=True, on_this_surface=None):
        """
        draw a draw_this_surface centered (or not) in the given coords
        """
        if on_this_surface is None:
            on_this_surface = self.screen
        x, y = disp_pos
        if center:
            on_this_surface.blit(draw_this_surface,
                                 (x - draw_this_surface.get_width() // 2, y - draw_this_surface.get_height() // 2))
        else:
            on_this_surface.blit(draw_this_surface, (x, y))
        return on_this_surface

    def draw_surfaces(self, surface_list):
        for surface in surface_list:
            self.draw_surface_screen(surface, c.CENTER, False)

    @staticmethod
    def draw_surface(draw_this_surface, on_this_surface, disp_pos=(0, 0), center=True, middle=False):
        """
        draw a draw_this_surface centered (or not) in the given coords
        """
        if middle:
            disp_pos = (on_this_surface.get_width() // 2, on_this_surface.get_height() // 2)

        x, y = disp_pos

        if center:
            on_this_surface.blit(draw_this_surface,
                                 (x - draw_this_surface.get_width() // 2, y - draw_this_surface.get_height() // 2))
        else:
            on_this_surface.blit(draw_this_surface, (x, y))

    @staticmethod
    def convert_to_mask(mask_surface, disp_pos, type_name, b_pos=None):
        """
        create and return the mask of a tile with the position of the tile in the display and not in the board
        """
        x, y = disp_pos
        tile_rect = mask_surface.get_rect(center=(x, y))
        # place mask itself
        tile_mask = pygame.mask.from_surface(mask_surface)
        return tile_rect, tile_mask, (x, y), type_name, b_pos

    # menus
    def create_menu(self, pos_list, text_list, sub_list, textures):
        """
        create a general menu used to create all the menu in game
        pos list and text list are two lists who needs to be the same lengh and are the informations of the buttons
        """

        menu_but_masks = []

        text_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        bg = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        for i in range(-3, 4):
            for j in range(-3, 4):

                text_str = None
                sub_str = None
                n = 0
                x = c.X_MID + (i * 3 * c.MENU_RADIUS / 2 - j * 3 * c.MENU_RADIUS / 2) * c.MENU_EDGE
                y = c.Y_MID + (i * c.MENU_UNIT + j * c.MENU_UNIT) * c.MENU_EDGE

                for k, pos in enumerate(pos_list):
                    if (i, j) == pos:
                        n = k + 1
                        text_str = text_list[k]
                        try:
                            sub_str = sub_list[k]
                        except IndexError:
                            pass
                        continue

                if n > 0:
                    but_tag = "but_" + str(n)
                    self.draw_surface_screen(textures.dflt["button"], (x, y), on_this_surface=bg)
                    text = textures.font["menu button"].render(text_str, True, textures.colors["button text"])
                    menu_but_masks.append(self.convert_to_mask(textures.dflt["button"], (x, y), but_tag))
                    self.draw_surface_screen(text, (x, y), on_this_surface=text_surface)
                    text = textures.font["menu button sub"].render(sub_str, True, textures.colors["button text sub"])
                    menu_but_masks.append(self.convert_to_mask(textures.dflt["button"], (x, y), but_tag))
                    self.draw_surface_screen(text, (x, y + 30), on_this_surface=text_surface)

                else:
                    self.draw_surface_screen(textures.dflt["bg hex"], (x, y), on_this_surface=bg)

        self.draw_surface_screen(textures.dflt["menu title"], c.TITLE_POS, on_this_surface=text_surface)
        self.draw_surface_screen(textures.dflt["menu sub 1"], c.SUB1_POS, on_this_surface=text_surface)

        # bg is the background, text_surface is the text overlay surface, menu_but_masks are the masks used for button
        return bg, text_surface, menu_but_masks

    def create_main_menu(self, textures):
        """
        create the surface and the masks used in the menu screen
        """

        pos_list = [(0, 1), (0, 0), (1, 1), (1, 0)]
        text_list = ["Tutorial", "Play offline", "Play online", "More infos"]
        sub = ["Soon", "", "Soon", "Git Hub"]

        bg, text_surface, menu_but_masks = self.create_menu(pos_list, text_list, sub, textures)

        return menu_but_masks, bg, text_surface

    def create_infos_menu(self, textures):
        """
        create the surface and the masks used in the menu screen
        """

        pos_list = [(0, 1), (1, 0), (0, 0), (1, 1)]
        text_list = ["Git Hub", "Website", "Back", "Quit game"]
        sub = ["Webpage", "In french", "To the menu", ""]

        bg, text_surface, menu_but_masks = self.create_menu(pos_list, text_list, sub, textures)

        return menu_but_masks, bg, text_surface

    def create_interrupt_menu(self, textures):
        """
        create the surface and the masks used in the menu screen
        """

        pos_list = [(0, 1), (0, 0), (1, 1), (1, 0)]
        text_list = ["Save", "Resume", "Quit", "Git Hub"]
        sub = ["Soon", "", "", "Web page"]

        bg, text_surface, menu_but_masks = self.create_menu(pos_list, text_list, sub, textures)

        return menu_but_masks, bg, text_surface

    # game related

    def draw_table(self, last_turn, turn, state, clock, textures):
        """
        draw the full table on the right of the screen
        """

        table = self.draw_states(turn, state, textures)

        your_turn = True

        for i in [c.TURN_STATE[turn],  c.TURN_STATE[last_turn]]:

            clock_surface = self.draw_clock(clock=clock[i], turn=your_turn, textures=textures)
            self.draw_surface_screen(draw_this_surface=clock_surface, disp_pos=c.CLOCK[i], on_this_surface=table, center=True)
            your_turn = False

        self.draw_surface_screen(table, c.TB, True)

    def draw_states(self, turn, state, textures):
        """
        on the table draw the states
        """

        table = pygame.Surface(c.TB_SIZE, pygame.SRCALPHA, 32)
        table.fill(textures.colors["infos"])

        self.draw_surface_screen(draw_this_surface=textures.write(turn), disp_pos=c.TURN_P, center=True, on_this_surface=table)
        self.draw_surface_screen(draw_this_surface=textures.write(state, font="game infos"), disp_pos=c.PROCESS_P, center=True,
                                 on_this_surface=table)

        return table

    def draw_clock(self, clock, turn, textures):

        stopwatch = pygame.Surface((200, 60), pygame.SRCALPHA, 32)

        if turn:
            stopwatch.fill(textures.colors["clock turn"])

        else:
            stopwatch.fill(textures.colors["clock not turn"])

        text = pygame.Surface((200, 60), pygame.SRCALPHA, 32)

        seconds = clock // 1000
        minutes = seconds // 60
        hours = minutes // 60

        minutes = minutes - 60 * hours
        seconds = seconds - 60 * minutes - 60**2 * hours
        tenth = "{:03d}".format(clock)[-3]

        # hours
        if hours != 0:
            pos = [20, 30]
            text, pos = self.draw_2_chr(hours, pos, text, textures)
            text, pos = self.draw_small_chr(":", pos, text, textures)
            text, pos = self.draw_2_chr(minutes, pos, text, textures)
            text, pos = self.draw_small_chr(".", pos, text, textures)
            text, pos = self.draw_tenth("{:02d}".format(seconds)[0], pos, text, textures)

        elif minutes == 0 and seconds <= 60:
            pos = [22, 30]
            text, pos = self.draw_2_chr(minutes, pos, text, textures)
            text, pos = self.draw_small_chr(":", pos, text, textures)
            text, pos = self.draw_2_chr(seconds, pos, text, textures)
            text, pos = self.draw_small_chr(".", pos, text, textures)
            text, pos = self.draw_tenth(tenth, pos, text, textures)

        else:
            pos = [46, 30]
            text, pos = self.draw_2_chr(minutes, pos, text, textures)
            text, pos = self.draw_small_chr(":", pos, text, textures)
            text, pos = self.draw_2_chr(seconds, pos, text, textures)

        pos = stopwatch.get_rect().center

        self.draw_surface_screen(text, pos, True, on_this_surface=stopwatch)

        return stopwatch

    def draw_2_chr(self, value, pos, text, textures):
        temp = "{:02d}".format(value)
        for char in temp:
            self.draw_surface_screen(textures.clock_1[char], pos, True, on_this_surface=text)
            pos[0] = pos[0] + 28

        return text, pos

    def draw_small_chr(self, value, pos, text, textures):
        self.draw_surface_screen(textures.clock_1[value], pos, True, on_this_surface=text)
        pos[0] = pos[0] + 20

        return text, pos

    def draw_tenth(self, value, pos, text, textures):

        self.draw_surface_screen(textures.clock_2[value], pos, True, on_this_surface=text)
        pos[0] = pos[0] + 15

        return text, pos

    def game_over(self, text, textures):

        if text is not None:

            rend_text = textures.font["default"].render(text, True, textures.colors["button_text"])
            self.draw_surface_screen(rend_text, (c.X_MID, c.Y_SIZE / 26))


class Board(Display):
    """
    Class about everything related to the board
    """

    def __init__(self):
        """
        Constructor
        """
        Display.__init__(self)
        self.coordinate_list = []
        self.pos_list = []
        self.disp_list = []
        self.mask_list = []
        self.tile_state = {}

        self.ways = {}
        self.eat = {}

        self.last_tile_pos = None

        self.screen_copy = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.mouse_interaction_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.ways_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.last_move_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        # find were to draw the board to fit in the middle
        self.board_origin = c.X_MID, (c.Y_SIZE-self.position((9, 9), origin=(0, 0))[1])/2

    def _get_last_tile(self):
        return self.last_tile_pos

    def _set_last_tile(self, pos):
        self.last_tile_pos = pos

    last_tile = property(_get_last_tile, _set_last_tile)

    def position(self, b_pos, origin=None):
        """
        convert position coordinates of the board from an orthonormal system to the specific system of the screen
        convert position from board (b_pos) to screen coordinate x, y (coords)
        """
        if origin is None:
            origin = self.board_origin
        a, b = b_pos
        xo, yo = origin
        x = xo + (a * 3 * c.R / 2 - b * 3 * c.R / 2) * c.MULT
        y = yo + (a * c.U + b * c.U) * c.MULT
        return x, y

    def create_board(self, color_bg, tile_1, tile_2, tile_mask):

        # create a list of all the possible position of the board under the form of tuple (x, y)
        # creating a 10 by 10 board

        image = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA)

        coords_bg = [self.position((4, 0)), self.position((0, 0)), self.position((0, 4)),
                     self.position((5, 9)), self.position((9, 9)), self.position((9, 5))]

        pygame.draw.polygon(image, color_bg, coords_bg)

        for i in range(10):
            for j in range(10):
                # remove unwanted cell in the corners
                if abs(j - i) >= 5:
                    continue
                # adding the right cells to the board (70 in total)
                else:
                    cell = i, j
                    disp_pos = self.position(cell)

                    if i % 5 == 2 or j % 5 == 2:
                        self.draw_surface_screen(tile_1, disp_pos, on_this_surface=image)
                    else:
                        self.draw_surface_screen(tile_2, disp_pos, on_this_surface=image)

                    self.pos_list.append(cell)
                    self.disp_list.append(disp_pos)

                    # create masks to detect if the mouse interact with the tiles
                    self.mask_list.append(self.convert_to_mask(tile_mask, disp_pos, "tile", b_pos=cell))

                    # create dict of all the states of the cells, by default False (no insect on it)
                    self.tile_state.update({cell: None})
        return image

    def tile(self, b_pos, insect):
        """
        give the state_string of a tile, pos = (x, y) and insect = True if the tile is insect
        """
        self.tile_state.update({b_pos: insect})

    def check_tile_move(self, insect_moving, new_pos):
        """
        check if the insect can go on this tile without his ant beeing attacked
        """
        pass

    def reset_surface(self, name):
        if name == "mouse interaction surface":
            self.mouse_interaction_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        elif name == "ways surface":
            self.ways_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

    def draw_tile_overview(self, mask_infos, textures):

        update = False
        disp_pos = mask_infos[2]
        tile_pos = mask_infos[4]

        # check if the tile is a new tile, else no update of the screen
        if self.last_tile != mask_infos[4]:
            self.reset_surface("mouse interaction surface")
            self.draw_surface_screen(
                textures.game["tile overview"], disp_pos, on_this_surface=self.mouse_interaction_surface)

            update = True
        self.last_tile_pos = mask_infos[4]

        return update, tile_pos

    def draw_last_move(self, pos_list, textures):

        # clean last move
        self.last_move_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        # add both pos of new move
        for pos in pos_list:
            self.draw_surface_screen(
                textures.game["tile move"], self.position(pos), on_this_surface=self.last_move_surface)
