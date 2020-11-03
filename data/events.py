"""Events class file"""

import pygame as pg


class Events:                                                      # 이벤트 클래스로서 플레이어의 이벤트처리를 담당하는 클래스
    """Events class, handles the events from the player 
    """

    def __init__(self):
        self.actions_keys = {                                      # 해당 키에 대한 이벤트 처리 즉, 내가 누르는 키에 대한 반응
            pg.K_ESCAPE: ("quit",),
            pg.K_RETURN: ("enter", "menu", "pause"),
            pg.K_F4: ("f4",),
            pg.K_UP: ("up",),
            pg.K_DOWN: ("down",),
            pg.K_RIGHT: ("right",),
            pg.K_LEFT: ("left",),
        }
        self.dir_keys = {
            pg.K_UP: "up",
            pg.K_DOWN: "down",
            pg.K_RIGHT: "right",
            pg.K_LEFT: "left",
        }
        self.opposite_dir = {
            "up": "down",
            "down": "up",
            "right": "left",
            "left": "right",
            None: None,
        }
        self.dir_list = []

    def get(self):                              # 반환하는 pygame에 대한 이벤트 처리
        """Handle pygame events to return
        corresponding game events
        """
        keys_down = pg.key.get_pressed()
        actions = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions.append("quit")
                continue
            if event.type == pg.KEYDOWN:
                if event.key in self.actions_keys:
                    actions.extend(self.actions_keys[event.key])
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                if event.key in self.dir_keys:
                    self.track_dir(event)
        if keys_down[pg.K_LALT] and "f4" in actions:
            actions.append("quit")

        return actions

    def track_dir(self, event):
        """Keeps track of directional key states"""     # 조작하는 방향키에 대한 상태를 확인하는 함수
        direction = self.dir_keys[event.key]
        if event.type == pg.KEYDOWN:
            self.dir_list.insert(0, direction)
        if event.type == pg.KEYUP:
            if direction in self.dir_list:
                self.dir_list.remove(direction)

    def calc_dir(self, snake_dir):                        # 새로룬 방향을 조작하는 상태에 대해서 반환함 방향 list에 대해 기준을 삼는다.
        """Return the new direction
        based on the direction list
        """
        for potential_dir in self.dir_list:
            if potential_dir != self.opposite_dir[snake_dir]:
                return potential_dir
        return None
