COLOR_WHITE = (255, 255, 255)
COLOR_WHITE_OPAQUE = (255, 255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_DARK_BLUE = (0, 16, 112)
COLOR_GREEN = (0, 255, 0)
COLOR_FONT_GREEN = (128, 240, 128)
COLOR_PURPLE = (100, 98, 88)
COLOR_SILVER = (192, 192, 192)
COLOR_ORINGE = (240, 144, 32)       # 友军
COLOR_LIGHTBLUE = (2, 208, 240)     # 敌军
MOVE_BG_COLOR = (0, 255, 0, 64)
MBINFO_BG_COLOR = (0, 0, 0, 140)
HITAREA_BG_COLOR = (176, 0, 0, 140)
HITAREA_BRIGHT_COLOR = (240, 0, 0, 140)
HITAREA_DARK_COLOR = (176, 0, 0, 140)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400
FPS = 100
UNIT_SIZE = 50
COLOR_KEY = (247, 0, 255)   # For all the bmp file under resource\pmap, background color
COLOR_KEY_TRANSPARENT = (247, 0, 255, 255)
MOVE_UNIT = 48
FIELD_UNIT_SIZE = 48        # on field, each character is 48 * 48
FIELD_ATK_UNIT_SIZE = 64    # on field, for unit_atk pic, it is 64 * 64
FIELD_PLAY_FRAME_LAST = 70   # on field, when playing act, every frame last 70 minisecond by default
FIELD_ATK_FRAME_LAST = 140   # on field, when playing act
FIELD_DIE_FLICK_LAST = 700
FIELD_INFO_LAST = 1500
FIELD_POLL_LAST = 400
FIELD_MOVE_FAST = 100
FIELD_MOVE_MEDIA = 400
FIELD_MOVE_SLOW = 800

MBINFO_DIALOG_WIDTH = 220   # map block dialog
MBINFO_DIALOG_HEIGHT = 140
MIINFO_DIALOG_WIDTH = 200   # map item dialog
MIINFO_DIALOG_HEIGHT = 105

# UNIT_MOV_LEFT_FRAME = 4     # This frame start from 0
# UNIT_MOV_RIGHT_FRAME = 4
# UNIT_MOV_DOWN_FRAME = 0
# UNIT_MOV_UP_FRAME = 2

FIELD_TROOP_US = 0          # On battle field, our troop
FIELD_TROOP_ENEMY = 1       # Enemy
FIELD_TROOP_ALLY = 2       # AllY

FONT_SONGTI = 'resource/font/FangZhengShuSong-GBK-1.ttf'
# FONT_NAME_CHN = 'resource/font/FangZhengHeiTI.ttf'
FONT_HEITI = 'resource/font/FangZhengZhengCuHeiTi.ttf'
FONT_JERSEY = 'resource/font/JerseyM54-aLX9.ttf'

TROOP_TYPE_NUM = 13         # 13 troop types

DEFAULT_MOVE_POWER = 4
DEFAULT_HIT_AREA = 'A'

MP_BAR_COLOR = '#ccd5ae'

# 1: face down move; 2: face down move; 3: face up move; 4: face up move; 5: face left move; 6: face left move;
# 7: face down still; 8: face up still; 9: face left still; 10: struggle; 11: more struggle
BF_CHAR_FRAME_MOVEDOWN = 1
BF_CHAR_FRAME_MOVEDOWN2 = 2
BF_CHAR_FRAME_MOVEUP = 3
BF_CHAR_FRAME_MOVEUP2 = 4
BF_CHAR_FRAME_MOVELEFT = 5
BF_CHAR_FRAME_MOVELEFT2 = 6
BF_CHAR_FRAME_DOWN = 7
BF_CHAR_FRAME_UP = 8
BF_CHAR_FRAME_LEFT = 9
BF_CHAR_FRAME_STRUGGLE = 10
BF_CHAR_FRAME_STRUGGLE2 = 11

BF_CHAR_FACE_LEFT = 0
BF_CHAR_FACE_RIGHT = 1
BF_CHAR_FACE_UP = 2
BF_CHAR_FACE_DOWN = 3

# for example: resource/unit_atk/弓兵.bmp; every action has 4 frames
BF_CHAR_FRAMEATK_DOWN = 1  
BF_CHAR_FRAMEATK_UP = 5  
BF_CHAR_FRAMEATK_LEFT = 9  
