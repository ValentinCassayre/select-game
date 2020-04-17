import math


# WINDOW
X_SIZE = 1080
Y_SIZE = 720
X_BASE = X_SIZE//2
Y_BASE = Y_SIZE//10
SCREEN_SIZE = (X_SIZE, Y_SIZE)
GAME_NAME = "Select!"

# FRAME RATE
FPS = 10

# BOARD
# CELLS
RADIUS = 32  # radius of the conscript circle that contain the apexes of the hexagon
UNIT = (2**5)*math.sqrt(3)  # radius of the circumscribed circle that contain the edges of the hexagon

# INSECTS
INSECT_LIST = ["bug_1", "bug_2"]  # they need to start with their role name : bug
INITIAL_POSITION = [(0, 0), (0, 1)]  # tuple with a (x, y) form

# PICTURES
# INSECTS PATHS
BUG_PATH = 'assets/insects/bug.png'
# BOARD PATHS
TILE_MASK_PATH = 'assets/board/tile_mask.png'
# ICON
ICON = 'assets/other/icon.png'

# RGB COLORS
# BOARD
BACKGROUND_COLOR = (255, 255, 255)
COLOR_TILE1 = (207, 107, 0)
COLOR_TILE2 = (169, 94, 30)

COLOR_OUTLINE = (245, 208, 122)

COLOR_HIGHLIGHT = (204, 180, 148)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)