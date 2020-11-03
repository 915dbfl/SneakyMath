"""View class file"""

import pygame

import data.constants as c
from data.textures import TEXTURES as textures
from data.tiles import Block
from data.functions import blit_alpha

# 표시되는 내용, 화면에 표시 될 때 처리하는 클래스
class View:
    #초기화
    def __init__(self):

        self.screen = pygame.display.set_mode(c.SCREEN_SIZE, pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.header = None
        self.field = None

    def init_textures(self):
        # 텍스쳐 초기화 후 창을 사용자 지정해주는 함수
        textures.create()
        pygame.display.set_icon(textures.dflt["icon"])
        self.screen.fill(textures.color["background"])
        pygame.display.set_caption(c.GAME_NAME)

    def tick(self, fps=c.FPS):
        """Sleep accordingly to the max FPS"""
        self.clock.tick(fps)

    @staticmethod
    def update():
        """Update the screen"""
        pygame.display.flip()

       #메뉴 화면 나타내기
    def draw_menu(self):
        self.screen.fill(textures.color["background"])
        textures.text(self, "title", c.GAME_NAME.upper())
        textures.text(
             # 시작 화면 설명란
            self, "menu", "Appuyer sur [Entrée] pour commencer ou [Echap] pour quitter" 
        )
        textures.text(
            self,
            "footnote",
            "© Créé par Romain avec l'aide de Natan "
            + "pour le prix Bernard Novelli des Trophées Tangente 2020 — Version "
            + c.VERSION,
        )

    # 화면이 멈췄을 때
    def draw_pause(self):
        self.screen.fill(textures.color["background"])
        textures.text(self, "pause", "Pause")
        textures.text(self, "menu", "Appuyer sur [Entrer] pour reprendre")

    # 게임 오버 화면 관련 함수
    def draw_game_over(self, player):
        overlay = pygame.Surface(c.SCREEN_SIZE)
        overlay.fill(textures.color["background"])
        overlay.set_alpha(210)
        self.screen.blit(overlay, (0, 0))
        textures.text(self, "game_over", "Game Over")
        textures.text(self, "new_score", "Score : " + str(player.score))
        if player.new_best:
            color = textures.color["snake"]
        else:
            color = textures.color["white_txt"]
        textures.text(
            self, "best_score", "Meilleur score : " + str(player.best_score), color
        )

    def draw_header(self, snake, player):
        """Draw the header and save it for the frames cycle"""
        self.screen.fill(textures.color["background"])
        self.header = textures.render_header(snake, player)
        self.screen.blit(self.header, (c.FIELD_OFFSET_X, 0))

    def draw_field(self, grid, snake, frames):
        #타일 모든 것을 화면에 나타내는 함수
        """Draw everything from the grid onto the screen"""
        field = textures.dflt["field"].copy()
        progress = frames / c.NB_FRAMES

        # 블록 그리는 함수
        for row in range(c.NB_ROWS):
            for col in range(c.NB_COLS):
                tile = grid[(col, row)]
                if isinstance(tile, Block):
                    field.blit(tile.image, tile.calc_rect())

        # 뱀 부분 그리기
        for part in reversed(snake.parts):
            if part is snake.tail and snake.inc < 0:
                alpha = round((1 - progress) * 255)
            else:
                alpha = None
            rects = []
            rect = part.calc_rect(progress, snake)
            rects.append(rect)
            rect = rect.copy()
            duplicate = False
            if rect.x < 0:
                rect.x += c.FIELD_W
                duplicate = True
            elif rect.x + c.T_W > c.FIELD_W:
                rect.x -= c.FIELD_W
                duplicate = True
            if rect.y < 0:
                rect.y += c.FIELD_H
                duplicate = True
            elif rect.y + c.T_H > c.FIELD_H:
                rect.y -= c.FIELD_H
                duplicate = True
            if duplicate:
                rects.append(rect)
            for rect in rects:
                blit_alpha(field, part.image, rect, alpha)
        self.field = field

    # 게임 화면 그리기
    def draw_game(self):
        self.screen.blit(self.field, (c.FIELD_OFFSET_X, c.FIELD_OFFSET_Y))
