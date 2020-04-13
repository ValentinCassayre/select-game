import math
import pygame


X_SIZE = 1080
Y_SIZE = 720
X_BASE = X_SIZE//2
Y_BASE = Y_SIZE//10
SCREEN_SIZE = (X_SIZE, Y_SIZE)
GAME_NAME = "Select!"

ALPHA = math.pi/3

FPS = 30

# Board
RADIUS = 32
UNIT = (2**5)*math.sqrt(3) # strange value found with geometrical simplifications

# INSECTS PATHS
BUG_PATH = 'assets/insects/bug.png'


# RGB COLORS
BACKGROUND_COLOR = (255, 255, 255)
COLOR_TILE1 = (207, 107, 0)
COLOR_TILE2 = (169, 94, 30)

COLOR_EDGE1 = (245, 208, 122)

COLOR_HIGHLIGHT = (204, 180, 148)