"""
All the constants of the game
Fact : i use // instead of / to avoid float
"""

from assets.math import Math

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
UNIT = Math.inscribed_rad(RADIUS)  # radius of the inscribed circle
EDGE_WIDTH = 1.1  # multiply radius by this to get the space between two tiles
# BOARD SIZE
B_W = 540
B_H = 614
BOARD_SIZE = (B_W, B_H)
# BOARD FIRST TILE POS (0, 0)
B_XO = X_MID
B_YO = (Y_SIZE - B_H)//2 + 1.2*UNIT
B_O = (B_XO, B_YO)
# BOARD PLACE POSITION (top left rect edge)
B_RECT_POS = (X_MID-B_W//2, Y_MID-B_H//2)

# STOPWATCH POS
SW = {0: (6*X_SIZE/7, Y_MID - 100), 1: (6*X_SIZE/7, Y_MID + 100)}

# TEXT POS
TB = (6*X_SIZE/7, Y_MID)
GT = (0, 10)
GS = (0, 20)

# GAME INFOS
GAME_NAME = "Select!"
# JUST TO KNOW WHICH ARE THE DIFFERENT STATES
GAME_STATE = {"choose insect": 0, "choose way": 1}
TURN_STATE = {"white": 0, "black": 1}

# PATHS
ICON = 'assets/other/icon.png'
FONTS = 'assets/fonts'
COLORS_DFLT = 'assets/default textures/colors.txt'
COLORS_CUST = 'assets/textures/colors.txt'
INSECTS = 'assets/default textures/insects/'
SCREENSHOTS = 'assets/screenshots/'

# TEST COLORS_DFLT
BACKGROUND_COLOR = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# TEXT PLACEMENTS
TITLE_POS = (X_MID, Y_SIZE/5)
SUB1_POS = (X_MID, Y_SIZE/3.4)

# TEXTS
SUB1 = "Game made by Valentin Cassayre"

MENU_RADIUS = 100
MENU_UNIT = Math.inscribed_rad(MENU_RADIUS)
MENU_EDGE = 1.1
