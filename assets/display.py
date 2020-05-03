"""
Display
"""

import pygame
import assets.consts as c


class Display:
    """
    Display mother class
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
        # Create the clock used to control the frame rate
        self.clock = pygame.time.Clock()

        self.menu_but_masks = []

    def draw_screen(self):
        """
        Create white background on the screen
        """
        self.screen.fill(c.BACKGROUND_COLOR)

    def draw_menu(self, textures):
        """
        Draw the menu screen
        """
        # Need to add the menu textures
        self.draw_screen()
        text_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        bg = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)

        for i in range(-3, 4):
            for j in range(-3, 4):

                text_str = None
                n = 0
                x = c.X_MID + (i * 3 * c.MENU_RADIUS / 2 - j * 3 * c.MENU_RADIUS / 2)*c.MENU_EDGE
                y = c.Y_MID + (i * c.MENU_UNIT + j * c.MENU_UNIT)*c.MENU_EDGE

                for k, pos in enumerate([(0, 1), (0, 0), (1, 1), (1, 0), (0, 2), (2, 0)]):
                    if (i, j) == pos:
                        n = k+1
                        text_str = ["Tutorial", "Play offline", "Play online", "Settings", "More infos", "Git Hub"][k]
                        continue

                if n > 0:
                    but_tag = "but_" + str(n)
                    self.draw_surface(textures.dflt["button"], (x, y), on_this_surface=bg)
                    text = textures.font["menu button"].render(text_str, True, textures.colors["button_text"])
                    self.menu_but_masks.append(self.convert_to_mask(textures.dflt["button"], (x, y), but_tag))
                    self.draw_surface(text, (x, y), on_this_surface=text_surface)

                else:
                    self.draw_surface(textures.dflt["bg_hex"], (x, y), on_this_surface=bg)

        self.draw_surface(textures.dflt["menu_title"], c.TITLE_POS, on_this_surface=text_surface)
        self.draw_surface(textures.dflt["menu_sub_1"], c.SUB1_POS, on_this_surface=text_surface)

        return self.menu_but_masks, bg, text_surface

    def draw_surface(self, draw_this_surface, disp_pos, center=True, on_this_surface=None):
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
            self.draw_surface(surface, c.CENTER, False)

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

        self.last_tile_pos = None

        self.screen_copy = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.mouse_interaction_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.ways_surface = self.screen_copy

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
        x = xo + (a*3*c.RADIUS/2 - b*3*c.RADIUS/2)*c.EDGE_WIDTH
        y = yo + (a*c.UNIT + b*c.UNIT)*c.EDGE_WIDTH
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
                        self.draw_surface(tile_1, disp_pos, on_this_surface=image)
                    else:
                        self.draw_surface(tile_2, disp_pos, on_this_surface=image)

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

    def check_tiles(self, insect_moving, tile_state=None, pos=None):
        ways = []
        eats = []

        if tile_state is None:
            tile_state = self.tile_state

        ant_attacked = None

        directions_way, directions_eat, eat_last = insect_moving.calc_directions(pos=pos)

        for direction in directions_way:
            cond = True
            i = 0
            while cond is True and i < len(direction):
                cell = direction[i]
                if cell in self.pos_list:
                    if tile_state[direction[i]] is None:
                        ways.append(direction[i])
                        i = i + 1
                    elif eat_last is True and tile_state[direction[i]].color != insect_moving.color:
                        if tile_state[direction[i]].king:
                            ant_attacked = tile_state[direction[i]]
                        else:
                            eats.append(direction[i])
                        cond = False
                    else:
                        cond = False
                else:
                    cond = False

        for direction in directions_eat:
            cond = True
            i = 0
            while cond is True and i < len(direction):
                cell = direction[i]
                if cell in self.pos_list:
                    insect_on_way = tile_state[direction[i]]
                    if insect_on_way is not None and insect_on_way.color != insect_moving.color:
                        if tile_state[direction[i]].king:
                            ant_attacked = tile_state[direction[i]]
                        else:
                            eats.append(direction[i])
                        i = i + 1
                    else:
                        cond = False
                else:
                    cond = False

        return ways, eats, ant_attacked

    def check_tile_move(self, insect_moving, new_pos):
        """
        check if the insect can go on this tile without his ant beeing attacked
        """
        pass

    def reset_surface(self, name):
        if name == "mouse_interaction_surface":
            self.mouse_interaction_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        elif name == "ways_surface":
            self.ways_surface = pygame.Surface(c.SCREEN_SIZE, pygame.SRCALPHA, 32)
        else:
            print("Error")

    def draw_tile_overview(self, mask_infos, textures):

        update = False
        disp_pos = mask_infos[2]
        tile_pos = mask_infos[4]

        # check if the tile is a new tile, else no update of the screen
        if self.last_tile != mask_infos[4]:
            self.reset_surface("mouse_interaction_surface")
            self.draw_surface(
                textures.game["tile_overview"], disp_pos, on_this_surface=self.mouse_interaction_surface)

            update = True
        self.last_tile_pos = mask_infos[4]

        return update, tile_pos
