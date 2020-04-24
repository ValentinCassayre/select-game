"""
All the constants of the game
Fact : i use // instead of / to avoid float
"""

import math


# WINDOW
X_SIZE = 1080
Y_SIZE = 720
SCREEN_SIZE = (X_SIZE, Y_SIZE)
X_MID = X_SIZE//2
Y_MID = Y_SIZE//2
MIDDLE = (X_MID, Y_MID)
CENTER = (0, 0)

# FRAME RATE
FPS = 100

# BOARD
# CELLS
RADIUS = 32  # radius of the conscript circle that contain the apexes of the hexagon
UNIT = (2**5)*math.sqrt(3)  # radius of the circumscribed circle that contain the edges of the hexagon
EDGE_WIDTH = 1.1  # multiply radius by this to get the space between two tiles
# BOARD SIZE
B_W = 540
B_H = 614
BOARD_SIZE = (B_W, B_H)
# BOARD FIRST TILE POS (0, 0)
B_XO = X_MID
B_YO = (Y_SIZE - B_H)//2 + 1.2*UNIT/2
B_O = (B_XO, B_YO)
# BOARD PLACE POSITION (top left rect edge)
B_RECT_POS = (X_MID-B_W//2, Y_MID-B_H//2)


# INSECTS
INSECT_LIST = ["bug_1", "bug_2"]  # they need to start with their role name : bug
INITIAL_POSITION = [(0, 0), (3, 5)]  # tuple with a (x, y) form

# GAME INFOS
GAME_NAME = "Select!"
# JUST TO KNOW WHICH ARE THE DIFFERENT STATES
GAME_STATE = {"choose insect": 0, "choose way": 1}
TURN_STATE = {"white": 0, "black": 1}

# PICTURES
# INSECTS PATHS
BUG_PATH = 'assets/textures/insects/bug.png'
# BOARD PATHS
TILE_MASK_PATH = 'assets/board/tile_mask.png'
# ICON
ICON = 'assets/other/icon.png'

# TEST COLORS
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)