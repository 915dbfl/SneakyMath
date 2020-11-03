"""Main program file"""

import pygame                               # pygame 선언

import data.constants as c
from data.events import Events
from data.grid import Grid
from data.player import Player
from data.snake import Snake
from data.view import View                 # data안에 있는 py들을 가져와 import함.


def main():
    """Main program"""

    pygame.init()                          # pygame 모듈을 사용하기 위한 초기화
    view = View()                          
    events = Events()
    player = Player()                      # import한 다른 클래스들을 각각 변수에 저장

    view.init_textures()
    view.update()
    player.retrieve_scores()               # view와 player 클래스 안에 있는 각각의 메서드를 호출 

    main_loop = True
    active_game = False
    prev_state = None                      # 어떤 상태를 말하는거 같은데 무얼 뜻하는지 잘 모르겠음. prev_state = False, True, 1, 0 등등 바꿔도 게임 구동에 이상이 없음 
    state = "MENU"                         # state 즉 상태의 default값 = "메뉴"

    # Main looop
    while main_loop:

        # Menu loop
        while main_loop and state == "MENU":

            if prev_state != state:
                view.draw_menu()
                view.update()
                active_game = False         # True로 바뀌면 변수 snake를 불러오지 못함. (UnboundLocalError:오류)
                prev_state = state
            else:
                view.tick()                 # view calss에서 tick 메서드를 불러와 최대 fps를 위한 절전모드

            actions = events.get()          # 이벤트 처리 get메서드를 변수에 저장
            if "quit" in actions:
                main_loop = False           
            if "enter" in actions:
                state = "GAME"              # quit 버튼을 누르면 main_loop = False로 바뀌며 게임 꺼짐 및 enter를 누르면 state는 game으로 전환되며 게임이 시작

        # Game loop
        while main_loop and state == "GAME":# 게임이 진행 될 때
            if prev_state != "PAUSE":
                frames = 0                  # prev_state의 상태가 pause로 변환 시 FPS는 0으로 고정되며 게임 일시정지

            if prev_state != state:
                if not active_game:
                    grid = Grid()
                    snake = Snake()
                    player.start_game()
                    snake.place_head(grid)
                    grid.generate()
                    direction = None        # 방향값 default = None 즉, 안움직임
                    active_game = True
                prev_state = state          # 즉 게임이 진행이 되기 위해 게임 내 요소들 등장 점수와 +,- 의 각 객체들을 불러와 화면에 띄워준다.

            view.draw_header(snake, player) # 헤더를 그려 프레임 주기에 맞게 저장 

            while frames < c.NB_FRAMES:     # NB_FRAMES는 지렁이의 속도 숫자가 낮으면 빨라짐 크면 느려짐

                view.draw_field(grid, snake, frames)    # 그리드 즉 화면 모든 타일에 관한것을 그린다. 
                view.draw_game()            # 게임을 그림
                view.update()               # 화면 업데이트
                view.tick()

                actions = events.get()
                if "quit" in actions:
                    main_loop = False
                if "pause" in actions:
                    state = "PAUSE"
                if not (main_loop and state == "GAME"):
                    break

                new_dir = events.calc_dir(snake.dir) # 새로운 방향전환을 위한 변수
                if new_dir:
                    direction = new_dir
                frames += 1

            if snake.dead:
                state = "GAME OVER"
            if not (main_loop and state == "GAME"):
                break
            if not direction:
                continue

            snake.place_head(grid)           # 게임 시작 시 나의 새로운 머리?가 위치하게 하는 함수
            snake.propagate(grid, direction, player.goal_reached)   # 머리부터 움직여 뒤에 부위가 하나씩 따라오게 하는 힘수
            player.calc_score(snake.parts)   # 점수 계산하는 함수
            snake.behind_trail(grid, player) # 나의 뱀 뒤에서 새 블록이 생성되는 것과 추가 또는 제거를 관리하는 함수
            snake.check_front(grid)          # 앞에서 어떤 타일을 발견 하는 지에 대해서 반응하는 함수

            snake.goal_reached(player)       # 목표에 도달했는지 확인하는 함수

            if player.goal_reached:         
                player.new_goal()            # 플레이어가 목표에 도달 할 시 새로운 목표 하달

        # Pause
        while main_loop and state == "PAUSE":

            if prev_state != state:
                view.draw_pause()             # 일시정시 화면
                view.update()
                prev_state = state
            else:
                view.tick()

            actions = events.get()
            if "quit" in actions:
                main_loop = False
            if "pause" in actions:
                state = "GAME"

        # Game over
        while main_loop and state == "GAME OVER":

            if prev_state != state:
                player.calc_score(snake.parts)
                player.compare_scores()
                view.draw_game_over(player)
                view.update()
                player.save_scores()
                prev_state = state             # 게임오버시 점수 계산과 이전 베스트 스코어와 비교를 하고 게임 오버 화면 출력한 후 내 스코어를 저장한다.
            else:
                view.tick()

            actions = events.get()
            if "quit" in actions:
                main_loop = False
            if "escape" in actions:
                state = "MENU"
            if "enter" in actions:
                state = "MENU"

    pygame.quit()
