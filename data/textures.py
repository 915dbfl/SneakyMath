"""Texture class file"""

import os

import pygame as pg

import data.constants as c
import data.textures_func as func
from data.functions import resource_path


class Textures:
    #텍스쳐, 폰트 등을 저장
    """Textures class, create and manage
    the textures of the game
    """

    def __init__(self):
        #초기화
        self.font = None
        self.color = None
        self.dflt = None
        self.text = None

    def create(self):
        #텍스쳐 생성
        """Create the textures and other attributes"""
        self.font = self.create_fonts()
        self.color = self.create_colors()
        self.dflt = self.create_dflts()
        self.text = self.create_texts

    @staticmethod
    def create_fonts():
        #게임 내 글자 폰트 관리
        """Create font dict, which stores
        all the fonts of the game
        """
        fonts = {}
        font_path = os.path.join(c.FONTS_PATH, "JosefinSans-SemiBold.ttf")
        font_path = resource_path(font_path)

        font = func.get_font(font_path, 2)
        fonts["pause"] = font
        fonts["game_over"] = font

        font = func.get_font(font_path, 1.2)
        fonts["new_score"] = font
        fonts["best_score"] = font

        font = func.get_font(font_path, 0.9)
        fonts["menu"] = font

        font = func.get_font(font_path)
        fonts["number"] = font

        font = func.get_font(font_path, 1.8)
        fonts["operation"] = font

        font_path.replace("SemiBold", "Regular")
        font = func.get_font(font_path, 2.5)
        fonts["title"] = font

        font = func.get_font(font_path, 0.5)
        fonts["footnote"] = font

        font = func.get_font(font_path, 0.7)
        fonts["stat"] = font

        return fonts

    def create_colors(self):
        #게임 내 색상 관리
        """Create the color dict, which stores
        all the colors of the game
        """
        colors = {}

        color = func.color_palette((50, 50, 50))
        colors["field"] = color
        #배경색

        colors["background"] = color[2]

        color = func.color_palette((120, 230, 120))
        colors["snake"] = color
        #뱀색

        color = func.color_palette((250, 250, 100))
        colors["filled"] = color
        #조건 만족시 변하는 뱀머리색

        color = func.color_palette((230, 230, 230))
        colors["white"] = color

        color = func.color_palette((230, 230, 230), 0.95)
        colors["white_txt"] = color

        color = func.color_palette((80, 80, 80), 0.9)
        colors["black_txt"] = color

        color = func.color_palette(func.nbr_color(1), 0.9)
        colors["small_number"] = color

        color = func.color_palette(func.nbr_color(9), 0.9)
        colors["big_number"] = color

        return colors

    def create_dflts(self):
        #게임 내 텍스쳐 관리
        """Create default textures dict, which stores
        all the default textures of the game
        """
        dflt = {}

        img = func.field_tile(self.color["field"])
        field_tile = img
        dflt["field_tile"] = img.convert()

        #배경 텍스쳐 폭, 높이, 이미지
        # ! self.screen.get_size()
        size = (c.FIELD_W, c.FIELD_H)
        img = pg.Surface(size)
        for col in range(c.NB_COLS):
            for row in range(c.NB_ROWS):
                coords = (c.T_W * col, c.T_H * row)
                img.blit(field_tile, coords)
        dflt["field"] = img.convert()

        #헤더 텍스쳐
        size = (c.HEADER_W, c.HEADER_H)
        color = self.color["background"]
        img = pg.Surface(size)
        img.fill(color)
        dflt["header"] = img.convert()

        #뱀 텍스쳐
        color = self.color["snake"]
        img = func.tile(color)
        body_part = img
        dflt["snake_part"] = img.convert_alpha()

        #노란색으로 변한 뱀 텍스쳐
        size = list(c.T_SIZE)
        size[0] += 2 * c.BORDER
        size[1] += 2 * c.BORDER
        radius = c.RADIUS * 2
        color = self.color["filled"]
        img = func.tile(color)
        dflt["filled_snake_part"] = img.convert_alpha()

        #맞는 블록 먹을때 먹는모션-초록색몸
        color = self.color["snake"]
        img = func.tile(color, size=size, rounded=radius)
        dflt["snake_part_eating"] = img.convert_alpha()

        #맞는 블록 먹을때 먹는모션-노란색몸
        color = self.color["filled"]
        img = func.tile(color, size=size, rounded=radius)
        dflt["filled_snake_part_eating"] = img.convert_alpha()

        img = body_part.copy()
        size = (0, 0)
        img = pg.Surface(size, pg.SRCALPHA, 32)
        img.fill((255, 255, 255))  # For some reason SRCALPHA is black as an icon
        icon = pg.transform.smoothscale(body_part, size)
        # icon.set_colorkey((255, 255, 255))
        img.blit(icon, (0, 0))
        dflt["icon"] = img.convert_alpha()

        font = self.font["operation"]
        color = self.color["black_txt"]
        
        text = func.relief_text("+", font, color)
        dflt["+"] = text.convert_alpha()

        text = func.relief_text("-", font, color)
        dflt["-"] = text.convert_alpha()

        text = func.relief_text("÷", font, color)
        dflt["÷"] = text.convert_alpha()

        text = func.relief_text("×", font, color)
        dflt["×"] = text.convert_alpha()

        text = func.relief_text("R", font, color)
        dflt["R"] = text.convert_alpha()



        #+블록 텍스쳐
        ope_img = dflt["field_tile"].copy()
        ope_img.blit(func.tile(self.color["white"]), (0, 0))
        img = ope_img.copy()
        text = dflt["+"].copy()
        rect = text.get_rect()
        rect.x = round((c.T_W - rect.w) / 2)
        rect.y = round((c.T_H - rect.h - c.S_H) / 2)
        img.blit(text, rect)
        dflt["operation_+"] = img.convert()

        #-블록 텍스쳐
        img = ope_img.copy()
        text = dflt["-"].copy()
        rect = text.get_rect()
        rect.x = round((c.T_W - rect.w) / 2)
        rect.y = round((c.T_H - rect.h - c.S_H) / 2)
        img.blit(text, rect)
        dflt["operation_-"] = img.convert()

        #/-블록 텍스쳐
        ope_img = dflt["field_tile"].copy()
        ope_img.blit(func.tile(self.color["white"]), (0, 0))
        img = ope_img.copy()
        text = dflt["÷"].copy()
        rect = text.get_rect()
        rect.x = round((c.T_W - rect.w) / 2)
        rect.y = round((c.T_H - rect.h - c.S_H) / 2)
        img.blit(text, rect)
        dflt["operation_÷"] = img.convert()

        #*-블록 텍스쳐
        img = ope_img.copy()
        text = dflt["×"].copy()
        rect = text.get_rect()
        rect.x = round((c.T_W - rect.w) / 2)
        rect.y = round((c.T_H - rect.h - c.S_H) / 2)
        img.blit(text, rect)
        dflt["operation_×"] = img.convert()

        # 리셋(R) -블록 텍스쳐
        ope_img = dflt["field_tile"].copy()
        ope_img.blit(func.tile(self.color["white"]), (0, 0))
        img = ope_img.copy()
        text = dflt["R"].copy()
        rect = text.get_rect()
        rect.x = round((c.T_W - rect.w) / 2)
        rect.y = round((c.T_H - rect.h - c.S_H) / 2)
        img.blit(text, rect)
        dflt["operation_R"] = img.convert()

        #숫자블록 텍스쳐
        font = self.font["number"]
        color = self.color["white_txt"]
        for nbr in range(1, 10):
            nbr_color = func.color_palette(func.nbr_color(nbr))
            img = dflt["field_tile"].copy()
            img.blit(func.tile(nbr_color), (0, 0))
            text = str(nbr)
            rendered = func.relief_text(text, font, color)
            rect = rendered.get_rect()
            rect.x = round((c.T_W - rect.w) / 2)
            rect.y = round((c.T_H - rect.h) / 2)
            img.blit(rendered, rect)
            dflt["number_" + text] = img.convert()

        return dflt

    #텍스트 관리
    def create_texts(self, view, font_name, text, color=None):
        """Render text on the screen
        in the given style
        """
        #타이틀 텍스트
        font = self.font[font_name]
        if font_name == "title":
            color = self.color["snake"]
            depth = c.S_W * 2
            rendered = func.relief_text(text, font, color, depth)
            coords = (c.SCREEN_W / 2, c.SCREEN_H / 4)
        #엔터누를시 나오는 퍼즈 텍스트
        if font_name == "pause":
            color = self.color["small_number"]
            rendered = func.relief_text(text, font, color)
            coords = (c.SCREEN_W / 2, c.SCREEN_H / 3)
        #하얀색 설명 문구들 텍스트-False일시 시스템 기본폰트
        if font_name == "menu":
            color = self.color["white_txt"][0]
            rendered = font.render(text, True, color)
            coords = (c.SCREEN_W / 2, 3 * c.SCREEN_H / 5)
        #게임오버 폰트
        if font_name == "game_over":
            color = self.color["big_number"]
            rendered = func.relief_text(text, font, color)
            coords = (c.SCREEN_W / 2, c.SCREEN_H / 3)
        #뉴 스코어 폰트
        if font_name == "new_score":
            color = self.color["white_txt"][0]
            rendered = font.render(text, True, color)
            coords = (c.SCREEN_W / 2, c.SCREEN_H * 0.6)
        #베스트 스코어 폰트
        if font_name == "best_score":
            color = self.color["white_txt"][0]
            rendered = font.render(text, True, color)
            coords = (c.SCREEN_W / 2, c.SCREEN_H * 0.7)
        #처음화면 카피라이트 폰트
        if font_name == "footnote":
            color = self.color["white_txt"][2]
            rendered = font.render(text, True, color)
            coords = (c.SCREEN_W / 2, 19.2 * c.SCREEN_H / 20)

        rect = rendered.get_rect()
        x_coord, y_coord = round(coords[0]), round(coords[1])
        coords = (x_coord - rect.centerx, y_coord - rect.centery)
        view.screen.blit(rendered.convert_alpha(), coords)
    #게임 헤더 텍스쳐 관리
    def render_header(self, snake, player):
        """Render the game header"""
        header = self.dflt["header"].copy()

        # Draw the size stat in a rectangle
        depth = round(c.DEPTH / 2)
        #TAILLE, OBJECTIF 창 텍스쳐 관리
        if player.goal_reached:
            color = self.color["snake"]
        else:
            color = self.color["white"]
        size = (round(c.T_W * 3.5), c.T_H)
        img = func.tile(color, size, depth)
        tile_img = img
        rect = img.get_rect()
        rect.x = round(c.HEADER_W / 3) - round(rect.w / 2)
        rect.y = c.HEADER_H - rect.h
        tile_rect = rect
        header.blit(img, rect)
        
        #TAILLE 숫자 관리
        text = str(len(snake))
        font = self.font["number"]
        color = self.color["black_txt"]
        nb_y = tile_rect.y + round(2.1 * c.S_H)
        img = func.relief_text(text, font, color, depth)
        rect = img.get_rect()
        rect.y = nb_y
        rect.x = tile_rect.right - c.T_W - round(3.0 * c.S_W)
        rect.x += round((c.T_W - rect.w) / 2)
        header.blit(img, rect)

        #TAILLE 관리
        text = "TAILLE"
        font = self.font["stat"]
        color = self.color["black_txt"]
        stat_y = tile_rect.y + round(2.8 * c.S_H)
        img = func.relief_text(text, font, color, depth)
        rect = img.get_rect()
        rect.y = stat_y
        rect.x = tile_rect.left + round(4.0 * c.S_W)
        header.blit(img, rect)

        # Increment
        # TAILLE 우측 연산되는 숫자 관리
        font = self.font["number"]
        color = self.color["white_txt"]
        if snake.inc != 0:
            text = str(snake.inc)
            if snake.inc > 0:
                text = "+" + text
            img = func.relief_text(text, font, color, depth)
            rect = img.get_rect()
            rect.y = nb_y
            rect.x = tile_rect.right + round(2.0 * c.S_W)
            header.blit(img, rect)

        # Goal
        img = tile_img
        rect = tile_rect
        rect.x = round(2 / 3 * c.HEADER_W) - round(rect.w / 2)
        tile_rect = rect
        header.blit(img, rect)
        #OBJECTIF 관리
        text = str(player.goal)
        color = self.color["black_txt"]
        img = func.relief_text(text, font, color, depth)
        rect = img.get_rect()
        rect.y = nb_y
        rect.x = tile_rect.right - c.T_W - round(3.0 * c.S_W)
        rect.x += round((c.T_W - rect.w) / 2)
        header.blit(img, rect)

        text = "OBJECTIF"
        font = self.font["stat"]
        img = func.relief_text(text, font, color, depth)
        rect = img.get_rect()
        rect.y = stat_y
        rect.x = tile_rect.x + round(4.0 * c.S_W)
        header.blit(img, rect)

        return header.convert()


TEXTURES = Textures()
