"""Global constants file"""

import pygame

# pygame 초기화
pygame.init()  # Needed to get screen resolution

# Infos
GAME_NAME = "SneakyMath"
VERSION = "1.2"
# path 설정
FILES_PATH = "data/files"
FONTS_PATH = "data/fonts"


# Screen 크기 조정
infoObject = pygame.display.Info()
SCREEN_W = infoObject.current_w
SCREEN_H = infoObject.current_h
SCREEN_SIZE = (SCREEN_W, SCREEN_H)

NB_COLS = 20 
# 전체 타일의 열수
NB_ROWS = 10
# 전체 타일의 행수
NB_TILES = NB_COLS * NB_ROWS
# 전체 타일의 수

T_L = min(SCREEN_W // NB_COLS, SCREEN_H // (NB_ROWS + 1))
# 타일의 넓이와 높이
T_W = T_L
T_H = T_L
T_SIZE = (T_W, T_H)
S_W = round(T_W / 10)
# 반올림된 값이 저장(round 함수)
S_H = round(T_H / 10)

# 화면에서의 타일부분의 넓이와 높이
FIELD_W = T_W * NB_COLS
FIELD_H = T_H * NB_ROWS

# 화면에서의 점수판 부분의 넓이와 높이
HEADER_W = FIELD_W
HEADER_H = SCREEN_H - FIELD_H

# ??
FIELD_OFFSET_X = round((SCREEN_W - FIELD_W) / 2)
FIELD_OFFSET_Y = HEADER_H


# View
FPS = 60
NB_FRAMES = 13

# Gameplay
SCORE_INC = 3


# Style
RADIUS = 0.2
FONT_SIZE = round(11 / 20 * T_W)
DEPTH = S_H
BORDER = S_W
CONTRAST = 0.9
