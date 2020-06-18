"""
Main game program files
Used only during a game
"""

import pygame
import assets.consts as c
from assets.display import Display
from assets.initial_layout import InitialLayout


class Game:
    """
    Class used to clean the main.py and allow to store the data and say what to do
    also allows to create online games
    """

    def __init__(self, board, textures, time):
        """
        needed parameter board : object from Board
        """

        # General

        self.state_string = "menu"
        self.process_string = "choose insect"

        self.turn = "white"
        self.last_turn = "black"

        self.loop = True  # main loop
        self.started = False  # game started ?

        # Board

        self.tile_pos = None
        self.tile_insect = None

        self.board = board
        self.textures = textures
        self.time = time

        self.setback = None

        self.last_move = []

        self.log = None

        self.changed_turn = True

        self.turn_number = 0
        self.color_number = 0

        self.board_saves = []

        # Clock

        self.player_stopwatch = [0, 0]
        self.last_check = [0, 0]
        self.check = [0, 0]
        self.player_clock = [300000, 300000]
        self.round_clock = [300000, 300000]
        self.clock_bol = True

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

        if self.process == "game ended":
            self.stop_clock()

        self.update_name()

    # allows to store the data and use it in main properly
    state = property(_get_state, _set_state)  # indicate which state the game is in
    process = property(_get_process, _set_process)  # indicate during a game what the players should do

    def start(self):
        """
        starts the game
        """
        # prepare the initial position of the insects
        for insect_data in InitialLayout.classic():
            insect = insect_data[0](insect_data[1], insect_data[2], self.textures.insect_path)
            # update tile
            self.board.tile(insect.pos, insect)

            # importing insect texture
            self.textures.save_insect(insect.full_name, insect.pict)

        self.update_ways()
        self.started = True

        self.start_clock()

    def stop(self):
        """
        stops the game loop
        """
        self.loop = False

    def change_turn(self):
        """
        change the turn
        """

        turn = self.last_turn
        self.last_turn = self.turn
        self.turn = turn

        self.update_name()
        self.update_ways()

        self.start_clock()

        self.changed_turn = True

        self.turn_number = self.turn_number + 1
        self.board_saves.append(self.board)

    def update_name(self):
        """
        update the window name
        """
        bond = " - "
        if self.state_string == "game":
            pygame.display.set_caption(c.GAME_NAME + bond +
                                       "In " + self.state_string + bond +
                                       self.turn.capitalize())
        else:
            pygame.display.set_caption(c.GAME_NAME + bond +
                                       self.state_string.capitalize())

    def select_insect(self, tile_pos):
        """
        select the insect if good color
        """

        # check any insect is on this tile
        if self.board.tile_state[tile_pos] is not None:

            # check if insect is owned by the player
            if self.board.tile_state[tile_pos].color == self.turn:

                return self.board.tile_state[tile_pos]

    def choose_insect(self, textures):
        """
        allows the player to select the tile on which there is the insect he want to move
        """
        # return the object of the tile insect if the insect can be selected
        self.tile_insect = self.select_insect(self.tile_pos)

        update = False
        selected_insect = None

        # check is something has been selected
        if self.tile_insect is not None:

            ways, eat = self.tile_insect.ways, self.tile_insect.eat

            # if the insect can't move
            if len(ways+eat) == 0:
                return update, selected_insect

            for way_cell in ways:
                self.board.draw_surface_screen(
                    textures.game["tile way"], self.board.position(way_cell), on_this_surface=self.board.ways_surface)

            for eat_cell in eat:
                self.board.draw_surface_screen(
                    textures.game["tile eat"], self.board.position(eat_cell), on_this_surface=self.board.ways_surface)

            update = True
            self.process = "choose way"

            selected_insect = self.tile_insect

        return update, selected_insect

    def choose_way(self, textures, drag=False):
        """
        allows the player to give the new position of the selected insect
        """
        reset = True

        if self.tile_insect is not None:

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

                self.kill(self.tile_insect, self.board.tile_state[self.tile_pos])

                # update tile after
                update = True
                self.process = "next turn"

                self.board.draw_last_move(self.last_move, textures)

            elif drag and self.tile_pos == self.tile_insect.pos:

                reset = False
                update = True
                self.process = "choose way"

            else:
                update = True
                self.process = "choose insect"

        else:
            update = True
            self.process = "choose insect"

        if reset:
            self.board.reset_surface("ways surface")

        return update, self.tile_insect

    # Movement of the insect on the board

    def move(self, insect, new_pos):
        # moving on board
        self.board.tile(insect.pos, None)
        self.board.tile(new_pos, insect)

        # moving object
        insect.pos = new_pos

    def kill(self, murderer, dead):
        self.board.tile(murderer.pos, None)
        murderer.pos = dead.pos

        # special killing -> killer gets killed with the dead insect
        if murderer.kamikaze:
            self.board.tile(dead.pos, None)

        # normal killing -> murderer replacing the dead insect
        else:
            self.board.tile(dead.pos, murderer)

    # movement related
    def update_ways(self):
        """
        update all the possible ways the insects can go
        """

        setback = None
        total_paths = []

        for tile in self.board.tile_state:

            if self.board.tile_state[tile] is not None:

                insect = self.board.tile_state[tile]

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
                            if self.board.tile_state[cell].ant is not True:
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
            self.log = "{} attacked !".format(self.turn.capitalize())

        if len(total_paths) == 0:
            if setback:
                self.log = self.turn, "{} lost ! Ant stuck".format(self.turn.capitalize())
            else:
                self.log = None, "Draw ! {} cannot move".format(self.turn.capitalize())

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

    def check_end_game(self):
        """
        check if there is someone who lost or if there is a draw
        """

        if self.log is not None:

            self.process = "end game"

    def save(self):
        """
        save current object
        """
        cond = True
        n = 1
        while cond:
            try:
                # file already exist ?
                open('assets/save/save {}.txt'.format(n), 'r')
            except FileNotFoundError:
                # if file doesn't exist we can save here
                self.open_file('assets/save/save {}.txt'.format(n))
                cond = False
            n = n + 1

    def open_file(self, file):
        """
        open and convert colors file
        """
        with open(file, 'w') as save:
            save.write(str(self.board_saves))
            save.close()

    # clock related

    def i(self):
        return c.TURN_STATE[self.turn]

    def start_clock(self):
        """
        start the clock of the player
        """
        self.clock_bol = True

        self.last_check[self.i()] = self.time.stopwatch.get_ticks()

    def update_clock(self):
        """
        update the clock value
        """
        i = self.turn_number%2
        if self.clock_bol:
            self.player_stopwatch[i] = self.time.stopwatch.get_ticks()-self.last_check[i]
            self.last_check[i] = self.time.stopwatch.get_ticks()
            self.player_clock[i] = self.player_clock[i]-self.player_stopwatch[i]

    def stop_clock(self):
        """
        block the clocks
        """
        self.clock_bol = False


class Time:
    """
    time
    """
    def __init__(self):

        self.clock = pygame.time.Clock()
        self.stopwatch = pygame.time

    def tick(self):
        """
        limit frame rate
        """
        self.clock.tick(c.FPS)


