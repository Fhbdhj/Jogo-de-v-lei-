# encoding : UTF-8

from enum import Enum
from pygame import *


# MAIN WINDOW
NOMINAL_RESOLUTION = (400, 320)
CAPTION_TITLE = "Volley-ball game"

FORCE_WINDOW_SCALE_FACTOR = 1  # None to disable or a float
IS_WINDOW_SCALE_FACTOR_2POW = True
IS_WINDOW_SCALE_FACTOR_INT = True
IS_WINDOW_IN_FULL_SCREEN_MODE = False

# TIME
NOMINAL_FRAME_RATE = 30
TIME_SPEED = 1  # < 1 to slow down, > 1 to speed up

# PHYSICS
G = 10

# CAMERA
CAMERA_POS = (11, 0, 3)
FOCUS_POINT = (0, 0, 3)
FOV_ANGLE = 60.

# WORLD
# court
COURT_DIM_X = 6
COURT_DIM_Y = 10
NET_HEIGHT_BTM = 1.5
NET_HEIGHT_TOP = 3

# ball
BALL_RADIUS = 0.5

# character
CHARACTER_W = 0.4
CHARACTER_H = 1


# INPUTS
class KeyState(Enum):
	RELEASED = 0
	JUST_PRESSED = 1
	PRESSED = 2
	JUST_RELEASED = 3


# PLAYER ACTIONS PARAMETERS
THROW_DURATION = 500    				# in ms
SERVE_DURATION = 500    				# in ms
JUMP_VELOCITY = 8       				# in m/s
SMASH_VELOCITY = 15     				# in m/s
DIVE_SPEED = 4							# in m/s
DIVE_SLIDE_DURATION = 250				# in ms
DIVE_DURATION_FOR_STANDING_UP = 500		# in ms

# THROW PARAMETERS
THROW_CENTER = Vector3(0, 3, BALL_RADIUS)
THROW_AMP_DIR = (2, 1.4)

SMASH_CENTER = Vector3(0, 4, BALL_RADIUS)
SMASH_AMP_DIR = (0, 1.4)

SERVE_CENTER = Vector3(0, 3.5, BALL_RADIUS)
SERVE_AMP_DIR = (2.4, 1.4)

DRAFT_THROW_HEIGHT = 4
DRAFT_DIRECTION_COEFFICIENT = 1.0


# actions
class PlayerAction(Enum):
	MOVE_LEFT = 0
	MOVE_RIGHT = 1
	MOVE_UP = 2
	MOVE_DOWN = 3
	THROW_BALL = 4
	JUMP = 5
	DIVE = 6
	CAMERA_MOVE_LEFT = 7
	CAMERA_MOVE_RIGHT = 8
	CAMERA_MOVE_UP = 9
	CAMERA_MOVE_DOWN = 10
	QUIT = 11
	PAUSE = 12
	SPACE_TEST = 13


# events
ACTION_EVENT = USEREVENT + 1
THROW_EVENT = USEREVENT + 2
RULES_BREAK_EVENT = USEREVENT + 3


# throwing type
class ThrowingType(Enum):
	THROW = 0
	SMASH = 1
	SERVE = 2
	DRAFT = 3
	
	
# human players id
class PlayerId(Enum):
	PLAYER_ID_ALL = 0
	PLAYER_ID_1 = 1
	PLAYER_ID_2 = 2
	
	
# bot id
class AIId(Enum):
	AI_ID_1 = 1
	AI_ID_2 = 2
	

class Team(Enum):
	LEFT = 1
	RIGHT = 2


# RULES
class RuleType(Enum):
	TOUCHES_NB = 1
	GROUND = 2
	UNDER_NET = 3
	
MAX_TOUCHES_NB = 3

	
# DIRECTORIES
FONT_DIR = "../assets/font/PressStart2P.ttf"


# COLORS
BKGND_TRANSPARENCY_COLOR = (1, 1, 1)  # color used for transparency
HUD_FONT_COLOR = (200, 200, 200)
DEBUG_TEXT_COLOR = (255, 255, 0)
BKGND_SCREEN_COLOR = (0, 0, 50)
