"""
Game class
"""


class Game:
    """
    Class used to clean the main.py and allow to store the data and say what to do
    """

    def __init__(self):
        # variables and default state
        self.state_string = "menu"
        self.process_string = "choose insect"
        self.turn_string = "white"

        self.loop = True  # main loop
        self.started = False  # game started ?

        self.insect_list = []

    # strings
    # state
    def _get_state(self):
        return self.state_string

    def _set_state(self, state):
        self.state_string = state

    # process
    def _get_process(self):
        return self.process_string

    def _set_process(self, process):
        self.process_string = process

    # turn
    def _get_turn(self):
        return self.turn_string

    def _set_turn(self, turn):
        self.turn_string = turn

    # allow to store the data and use it in main properly
    state = property(_get_state, _set_state)  # indicate which state the game is in
    process = property(_get_process, _set_process)  # indicate during a game what the players should do
    turn = property(_get_turn, _set_turn)  # indicate which player can play

    # lists
    # insects
    def _get_insects(self):
        return self.insect_list

    def _set_insects(self, insects):
        self.insect_list = insects

    insects = property(_get_insects, _set_insects)

    def stop(self):
        self.loop = False  # stop the main loop
