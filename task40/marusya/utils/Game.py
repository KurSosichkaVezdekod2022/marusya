from random import randint
from collections import deque
from copy import deepcopy


class Board:
    def __init__(self):
        self.w = 20
        self.h = 10
        self.snake = None
        self.apple_pos = None
        self.score = 0
        self.game_running = True
        self.accepted_moves = {'l': ['u', 'd', 'l'],
                              'r': ['u', 'd', 'r'],
                              'u': ['u', 'l', 'r'],
                              'd': ['d', 'l', 'r']}

    def start(self):
        self.snake = Snake()
        self.score = 0
        self.game_running = True
        self.apple_spawn()

    def get_state(self):
        apple = '@'
        snake_part = '#'
        snake_head = '$'
        clear_cell = '*'
        draw_board = list()
        for row in range(self.h):
            draw_row = list()
            for col in range(self.w):
                cell = [row, col]
                if cell in self.snake.snake_parts:
                    if cell == self.snake.head_pos:
                        draw_row.append(snake_head)
                    else:
                        draw_row.append(snake_part)
                elif cell == self.apple_pos:
                    draw_row.append(apple)
                else:
                    draw_row.append(clear_cell)
            draw_board.append(' '.join(draw_row))
        print(self.snake.snake_parts)
        return '\n'.join(draw_board)

    def apple_spawn(self):
        self.apple_pos = [randint(0, 9), randint(0, 19)]

    def move(self, direction):
        if direction not in self.accepted_moves[self.snake.current_direction]:
            return False
        self.snake.current_direction = direction
        self.step()

    def step(self):
        next_head_pos = self.snake.head_pos
        if self.snake.current_direction == 'l':
            next_head_pos[1] -= 1
        elif self.snake.current_direction == 'r':
            next_head_pos[1] += 1
        elif self.snake.current_direction == 'u':
            next_head_pos[0] -= 1
        elif self.snake.current_direction == 'd':
            next_head_pos[0] += 1
        if self.check_border_collide(next_head_pos) and self.check_tail_collide(next_head_pos):
            self.snake.head_pos = deepcopy(next_head_pos)
            self.snake.snake_parts.appendleft(deepcopy(next_head_pos))
            prev = self.snake.snake_parts.pop()
            self.check_apple_collide(prev)
        else:
            self.game_running = False

    def check_border_collide(self, position):
        if position[1] < 0 or position[1] >= self.w or position[0] < 0 or position[0] >= self.h:
            return False
        return True

    def check_tail_collide(self, position):
        if position in self.snake.snake_parts[1:]:
            return False
        return True

    def check_apple_collide(self, part):
        if self.snake.head_pos == self.apple_pos:
            self.score += 1
            self.snake.length += 1
            self.snake.snake_parts.append(part)
            self.apple_spawn()


class Snake:
    def __init__(self):
        self.length = 3
        self.head_pos = [randint(2, 7), randint(5, 15)]
        self.snake_parts = deque()
        for i in range(self.length):
            part = deepcopy(self.head_pos)
            part[1] += i
            self.snake_parts.append(deepcopy(part))
        self.current_direction = 'l'
