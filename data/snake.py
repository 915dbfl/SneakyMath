"""Snake class file"""

import random

import data.constants as c
from data.tiles import SnakePart, Number, Operation

# 뱀 관련 클래스
class Snake:
    
    #초기화
    def __init__(self):
        self.dead = False
        self.inc = 4
        x_pos = c.NB_COLS // 2 - random.randint(0, (c.NB_COLS + 1) % 2)
        y_pos = c.NB_ROWS // 2 - random.randint(0, (c.NB_ROWS + 1) % 2)
        self.parts = [SnakePart((x_pos, y_pos))]
        self.behind_queue = []
        self.behind_pos = None
        self.ope = "change to +"

    def __len__(self):
        return len(self.parts)
    #머리
    def _get_head(self):
        return self.parts[0]
    #꼬리
    def _get_tail(self):
        return self.parts[-1]

    def _get_dir(self):
        if self.parts:
            return self.head.dir
        return None

    head = property(_get_head)
    tail = property(_get_tail)
    dir = property(_get_dir)

    def place_head(self, grid):
        #머리관련 텍스쳐 변경하는 함수
        grid[self.head.pos] = self.head
        if self.ope.startswith("change"):
            self.ope = self.ope[-1]
            self.head.ope = self.ope
            self.head.update_image()

    def propagate(self, grid, direction, eating):
        # 머리부터 시작하여 신체부위를 하나씩 이동 시키는 함수
        for part in self.parts:
            if part == self.tail:
                self.behind_pos = part.pos
            grid[part.pos] = None
            prev_dir = part.dir
            part.dir = direction
            part.move()
            if part is not self.head:
                grid[part.pos] = part
            direction = prev_dir

            prev_eating = part.eating
            part.eating = eating
            eating = prev_eating

            if part.eating and not part.filled:

                part.filled = True
                eating = False
                if part.eating >= c.SCORE_INC:
                    part.eating = False
                else:
                    if not part.eating:
                        part.eating = True
                    else:
                        part.eating += 1

            part.update_image()

    def behind_trail(self, grid, player):
        # 뱀 뒤에 있는 것들을 처리하는 함수(신체부위추가 또는 제거, 새블록)
        if self.behind_queue and not self.inc:
            grid[self.behind_pos] = self.behind_queue.pop(0)
        if self.inc > 0:
            self.parts.append(SnakePart())
            grid[(self.behind_pos)] = self.tail
            self.inc -= 1
        elif self.inc < 0:
            removed_part = self.parts.pop(-1)
            grid[removed_part.pos] = None
            self.behind_pos = removed_part.pos
            self.inc += 1
            if not self.parts:
                self.dead = True

    def check_front(self, grid):
        # 타일들을 확인하고 먹은 블록에 따라 반응함
        if not self.parts:
            return
        front_tile = grid[self.head.pos]
        if front_tile:
            # 숫자를 먹었을 때
            if isinstance(front_tile, Number):
                if "+" in self.ope: # + 블록을 먹었을 때
                    print(self.inc)
                    self.inc += front_tile.value
                    print(self.inc)
                    nbr_new = 2
                elif "-" in self.ope: # - 블록을 먹었을 때
                    print(self.inc)
                    self.inc -= front_tile.value
                    print(self.inc)
                    nbr_new = 2
                elif "÷" in self.ope: # / 블록을 먹었을 때
                    print(len(self))
                    self.inc -= (len(self) - (int)(len(self)/front_tile.value))
                    print(self.inc)
                    nbr_new = 2
                elif "×" in self.ope: # * 블록을 먹었을 때(먹은 블록의 두배 수가 늘어난다.)
                    print(self.inc)
                    self.inc += front_tile.value*2
                    print(self.inc)
                    nbr_new = 2
                elif "R" in self.ope: # R 블록 먹었을 때
                    self.inc = 0
                    nbr_new = 2

                for _ in range(nbr_new):
                    self.behind_queue.append(Number())
                    
            # 블록을 먹었을 때
            if isinstance(front_tile, Operation):
                self.ope = "change to " + front_tile.ope
                if front_tile.ope == "+":
                    self.behind_queue.append(Operation("-"))
                elif front_tile.ope == "-":
                    self.behind_queue.append(Operation("+"))
                elif front_tile.ope == "÷":
                    self.behind_queue.append(Operation("×"))
                elif front_tile.ope == "×":
                    self.behind_queue.append(Operation("÷"))
                elif front_tile.ope == "R":
                    self.behind_queue.append(Operation("R"))
                    self.__init__()
            
            # 뱀 몸부분에 닿았을 때
            elif front_tile in self.parts:
                self.dead = True

    def goal_reached(self, player):
        #Goal에 도달했는지 확인하는 함수
        if len(self) == player.goal and not self.inc:
            player.goal_reached = True         # 도달

            n_nbrs = sum(isinstance(block, Number) for block in self.behind_queue)
            new_n_nbrs = round(n_nbrs / 2)
            new_behind = []
            for block in self.behind_queue:
                if new_n_nbrs > 0 and isinstance(block, Number):
                    new_n_nbrs -= 1
                else:
                    new_behind.append(block)
            self.behind_queue = new_behind
