"""
Game class
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

        self.color_dict = {"white": 0, "black": 1}

        self.loop = True  # main loop
        self.started = False  # game started ?

        self.insect_list = []
        self.ways_list = []
        self.eat_list = []

        self.tile_pos = None
        self.tile_insect = None

        self.board = board

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
        if self.turn == "white":
            self.turn = "black"
        elif self.turn == "black":
            self.turn = "white"
        self.update_name()
        self.update_ways()
        self.update_list()

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

    def update_ways(self):
        """
        update all the possible ways the insects can go
        """

        total_ways = [0, 0]
        ins_a = None

        for insect in self.insects:
            ways, eat, insect_attacked = self.board.check_tiles(insect)
            insect.update_directions((ways, eat))

            total_ways[self.color_dict[insect.color]] = total_ways[self.color_dict[insect.color]] + len(ways) + len(eat)

            if insect_attacked is not None:
                ins_a = insect_attacked

        # check if the one who needs to play can play
        if total_ways[self.color_dict[self.turn]] == 0:
            print("Game stopped ! {} cannot move".format(self.turn))
            self.stop()

    def choose_insect(self, board, textures):
        # return the object of the tile insect if the insect can be selected
        self.tile_insect = self.select_insect(self.tile_pos)

        update = False

        # check is something has been selected
        if self.tile_insect is not None:

            ways, eat = self.tile_insect.ways, self.tile_insect.eat

            for way_cell in ways:
                board.draw_surface(
                    board.ways_surface,
                    textures.game["tile_way"],
                    board.position(way_cell))

            for eat_cell in eat:
                board.draw_surface(
                    board.ways_surface,
                    textures.game["tile_eat"],
                    board.position(eat_cell))

            update = True
            self.process = "choose way"

        return update

    def choose_way(self, board):

        # just moove
        if self.tile_pos in self.tile_insect.ways:
            board.tile(self.tile_insect.pos, None)
            self.tile_insect.pos = self.tile_pos
            board.tile(self.tile_insect.pos, self.tile_insect)
            update = True
            self.process = "next turn"

        # moove and kill
        elif self.tile_pos in self.tile_insect.eat:
            dead_insect = board.tile_state[self.tile_pos]
            self.tile_insect.kill(dead_insect)

            # update tile before
            board.tile(self.tile_insect.pos, None)
            # move insect
            self.tile_insect.pos = self.tile_pos
            # update tile after
            board.tile(self.tile_insect.pos, self.tile_insect)
            update = True
            self.process = "next turn"

        else:
            update = True
            self.process = "choose insect"

        board.reset_surface("ways_surface")
        return update
