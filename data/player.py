"""Player class file"""

import math
import os
import pickle
import random

import data.constants as c
from data.functions import resource_path


class Player:
    """Player class"""

    def __init__(self):
        self.score = 0
        self.best_score = 0
        self.new_best = False
        self.scores_path = resource_path(os.path.join(c.FILES_PATH, "scores"))
        self.goal = None
        self.goal_reached = False                                   # 점수와 베스트점수 목표 등을 초기화 하고 받는다.

    def retrieve_scores(self):
        """Retrieve scores from the score file"""
        if not os.path.isdir(resource_path(c.FILES_PATH)):          # FILES_PATH 에는 경로가 저장 되어 있음
            os.makedirs(resource_path(c.FILES_PATH))
        if os.path.isfile(self.scores_path):
            with open(self.scores_path, "rb") as score_file:
                unpickler = pickle.Unpickler(score_file)
                self.score = unpickler.load()
                self.best_score = unpickler.load()                  # 저장되어 있는 점수 파일 디텍토리를 찾아 이전 점수를 검색한다. 

    def save_scores(self):
        """Write scores to the score file"""
        with open(self.scores_path, "wb") as score_file:
            pickler = pickle.Pickler(score_file)
            pickler.dump(self.score)
            pickler.dump(self.best_score)                           # 점수 파일에 잠수를 기록하여 저장한다.

    def start_game(self):
        """Start the game reseting the score and the goal"""
        self.score = 0
        self.goal = 0
        self.new_goal()                                             # 게임 시작 시 점수와 목표점수를 초기화 하고 새로운 목표를 하달한다.

    def new_goal(self):
        """Generate a new goal"""                                   # 목표 달성시 새로운 목표 하달

        # 1st code
        # (int(str(score)[::-1]) - 1) % 50 + 1

        # 2nd code
        # return (goal + score - 1) % (35 + round(score / 15)) + 1

        # 3rd code
        # bound = 8 + round(1.5 * math.sqrt(self.score))
        # diff = min(40, 3 + self.score ** 1.2 // 70)
        # new_goal = self.goal
        # while (new_goal + diff) > self.goal > (new_goal - diff):
        #     new_goal = random.randint(
        #         max(self.score + c.SCORE_INC, min(15, self.goal - bound)),
        #         min(
        #             max(self.goal + bound, 20), 35 + math.floor(math.sqrt(self.score)),
        #         ),
        #     )
        # self.goal = new_goal

        mini = self.score + c.SCORE_INC * 2                         # SCORE_INC 숫자를 늘릴 시 목표 점수가 걷잡을 수 없이 커지게 됨
        diff = 3 + round(self.score ** 1.2 / 20)
        new_goal = self.goal
        while (new_goal + diff) > self.goal > (new_goal - diff):
            new_goal = random.randint(mini, min(c.NB_TILES, round(mini ** 1.1 + 10)))
        self.goal = new_goal                                        # 목표에 도달시 새로운 목표 점수의 계산

    def calc_score(self, parts):
        """Calculate the score"""
        self.score = sum([part.filled for part in parts])
        self.goal_reached = False                                   # 점수 계산 함수

    def compare_scores(self):
        """Determine if the score is a new best"""
        if self.score > self.best_score:
            self.best_score = self.score
            self.new_best = True                                    # 현 점수와 베스트 점수를 비교하는 함수
