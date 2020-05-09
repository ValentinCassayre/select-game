"""
Main game program files
Used only during a game
"""

import pygame
import assets.consts as c


class Game:
    """
    Class used to clean the main.py and allow to store the data and say what to do
    """

    def __init__(self, board):
        # variables and default state
        self.state_string = "menu"
        self.process_string = "choose insect"

        self.turn = "white"
        self.last_turn = "black"

        self.color_dict = {"white": 0, "black": 1}

        self.loop = True  # main loop
        self.started = False  # game started ?

        self.insect_list = []
        self.ways_list = []
        self.eat_list = []

        self.tile_pos = None
        self.tile_insect = None

        self.board = board

        self.setback = None

        self.test = None

        self.last_setback = None

        self.last_move = []

        self.end_game = None

        self.changed_turn = True

        # create the clock used to control the frame rate and the stopwatch
        self.clock = pygame.time.Clock()

        self.player_stopwatch = [0, 0]
        self.last_check = [0, 0]
        self.player_clock = [60000, 600000]

        self.turn_number = 0

        self.board_saves = []

    # strings
    # state
    def _get_state(self):
        return self.state_string

    def _set_state(self, state):
        self.state_string = state
        self.update_name()

    # process
    def _get_process(self):
        return self.process_string

    def _set_process(self, process):

        self.process_string = process

        # prepare for next turn
        if self.process == "next turn":

            self.process = "choose insect"
            self.change_turn()

        self.update_name()

    # allow to store the data and use it in main properly
    state = property(_get_state, _set_state)  # indicate which state the game is in
    process = property(_get_process, _set_process)  # indicate during a game what the players should do

    # lists
    # insects
    def _get_insects(self):
        return self.insect_list

    def _set_insects(self, insects):
        self.insect_list = insects

    insects = property(_get_insects, _set_insects)

    def stop(self):
        self.loop = False  # stop the main loop

    def change_turn(self):

        turn = self.last_turn
        self.last_turn = self.turn
        self.turn = turn

        self.update_name()
        self.update_ways()
        self.update_list()

        self.start_clock()

        self.changed_turn = True

        self.turn_number = self.turn_number + 1

    def update_name(self):
        """
        update the window name
        """
        bond = " - "
        if self.state_string == "game":
            pygame.display.set_caption(c.GAME_NAME + bond +
                                       "In " + self.state_string + bond +
                                       self.turn.capitalize() + bond +
                                       self.process_string.capitalize())
        else:
            pygame.display.set_caption(c.GAME_NAME + bond +
                                       self.state_string.capitalize())

    def update_list(self):
        for insect in self.insects:
            if insect.alive is False:
                self.insects.remove(insect)

    def start_clock(self):

        i = c.TURN_STATE[self.turn]

        time = pygame.time.get_ticks()
        self.last_check[i] = time

    def update_clock(self):

        time = pygame.time.get_ticks()

        i = c.TURN_STATE[self.turn]

        self.player_stopwatch[i] = time - self.last_check[i]

        self.player_clock[i] = self.player_clock[i] - self.player_stopwatch[i]

        self.last_check[i] = time

    def select_insect(self, tile_pos):
        """
        select the insect if good color
        """

        # check any insect is on this tile
        for insect in self.insects:

            if insect.pos == tile_pos:
                tile_insect = insect

                # check if insect is owned by the player
                if insect.color == self.turn:

                    return tile_insect

    def choose_insect(self, board, textures):
        # return the object of the tile insect if the insect can be selected
        self.tile_insect = self.select_insect(self.tile_pos)

        update = False

        # check is something has been selected
        if self.tile_insect is not None:

            ways, eat = self.tile_insect.ways, self.tile_insect.eat

            # if the insect can't move
            if len(ways+eat) == 0:
                return False

            for way_cell in ways:
                board.draw_surface(
                    textures.game["tile_way"], board.position(way_cell), on_this_surface=board.ways_surface)

            for eat_cell in eat:
                board.draw_surface(
                    textures.game["tile_eat"], board.position(eat_cell), on_this_surface=board.ways_surface)

            update = True
            self.process = "choose way"

        return update

    def choose_way(self, board, textures):
        update = False

        # just moove
        if self.tile_pos in self.tile_insect.ways:
            self.last_move = self.tile_insect.pos, self.tile_pos

            self.move(self.tile_insect, self.tile_pos)

            update = True
            self.process = "next turn"

            self.board.draw_last_move(self.last_move, textures)

        # moove and kill
        elif self.tile_pos in self.tile_insect.eat:
            self.last_move = self.tile_insect.pos, self.tile_pos

            dead_insect = board.tile_state[self.tile_pos]
            self.kill(self.tile_insect, dead_insect)

            # update tile after
            board.tile(self.tile_insect.pos, self.tile_insect)
            update = True
            self.process = "next turn"

            self.board.draw_last_move(self.last_move, textures)

        else:
            update = True
            self.process = "choose insect"

        board.reset_surface("ways_surface")

        return update

    def move(self, insect, new_pos):
        self.board.tile(self.tile_insect.pos, None)
        insect.pos = new_pos
        self.board.tile(self.tile_insect.pos, self.tile_insect)

    def kill(self, murderer, dead):
        self.board.tile(murderer.pos, None)
        try:
            self.insects.remove(dead)

        except ValueError:
            print("Value error in game.kill with the {} insect in pos {}".format(murderer.color, murderer.pos))

        murderer.kill(dead)
        if murderer.kamikaze:
            self.board.tile(dead.pos, None)
            murderer.killed()
            self.insects.remove(murderer)
        else:
            murderer.pos = dead.pos
            self.board.tile(murderer.pos, murderer)

    # movement related
    def update_ways(self):
        """
        update all the possible ways the insects can go
        """

        setback = None
        total_paths = []

        for insect in self.insects:
            ways, eat = self.check_obstacle(insect)

            if insect.color == self.turn:  # check ways

                new_ways, new_eat = [], []

                for cell in ways:

                    # check and remove illegal moves
                    if not self.removed_illegal_moves(insect, cell):
                        new_ways.append(cell)

                for cell in eat:

                    # check and remove illegal moves
                    if not self.removed_illegal_moves(insect, cell):
                        new_eat.append(cell)

                insect.ways = new_ways
                insect.eat = new_eat

                for cell in new_ways + new_eat:
                    total_paths.append(cell)

            else:  # check setback

                for cell in eat:

                    # check setback
                    if self.board.tile_state[cell].color != insect.color and self.board.tile_state[cell].ant:
                        setback = self.board.tile_state[cell]

        if setback is None:
            self.setback = None
        else:
            self.setback = setback

        if len(total_paths) == 0:
            if setback:
                print("LOST")
                self.end_game = "{} lost".format(self.turn)
            else:
                print("DRAW")
                self.end_game = "draw ({} cannot move and not setback)".format(self.turn)

    def removed_illegal_moves(self, insect, new_pos):
        """
        check if this move is an illegal move
        illegal move mean it set its own ant into setback
        """

        temp = self.board.tile_state.copy()
        temp.update({insect.pos: None})
        temp.update({new_pos: insect})

        for cell in self.board.pos_list:

            insect_attacking = temp[cell]

            # check if someone on it, and if it is an enemy
            if insect_attacking is not None and insect_attacking.color != insect.color:

                # get all the possible path he can get
                paths = self.check_obstacle(temp[cell], temp, paths=True)

                # check them
                for pot_attack_pos in paths:

                    insect_attacked = temp[pot_attack_pos]

                    # check if something on cell, check if there is an opponent on it, and if it is an ant
                    if insect_attacked is not None and insect_attacked.color == insect.color and insect_attacked.ant:
                        # if i split the conditions i can rescue some helpful information
                        # as how many insect it can attack

                        # it is an illegal move because in this case the ant of the insect is attacked by the opponent
                        return True

        # if the method gets to this place it means there is no illegal moves in here
        return False

    def check_obstacle(self, insect, board=None, paths=False):
        """
        check if the insect can go on this tile
        check if the tile is on the board
        check if there is no obstacle or another insect to kill
        """

        if board is None:
            board = self.board.tile_state

        directions_way, pos_eat, eat_last = insect.calc_directions(pos=None)
        ways, eat = [], []

        for direction in directions_way:
            can_continue = True
            i = 0

            # each direction is a list of possible cells
            while can_continue and i < len(direction):
                cell = direction[i]
                i = i + 1

                # check if tile exist and if there is obstacle on it
                if cell in self.board.pos_list:
                    if board[cell] is None:
                        # nothing on this cell
                        ways.append(cell)

                    else:
                        if eat_last and board[cell].color != insect.color:
                            eat.append(cell)
                        can_continue = False

                else:
                    can_continue = False

        for cell in pos_eat:
            # check if tile exist and if there is someone to eat on it
            if cell in self.board.pos_list and board[cell] is not None:
                if board[cell].color != insect.color:

                    eat.append(cell)

                else:
                    # same team so dont eat him
                    pass

        # return every pos this insect can normally go
        if paths:
            return ways + eat
        else:
            return ways, eat

    def check_turn(self):

        if self.changed_turn:
            self.changed_turn = False
            return True

        else:
            return False


class Tutorial(Game):
    """
    the tutorial apply lot of normal game rules but to have a better understanding in the tutorial mod there is text,
    auto move and less insects
    """
    def __init__(self, board):
        Game.__init__(self, board)
        self.n = 0

    def start(self):
        self.state = "tutorial"


