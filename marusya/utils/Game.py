import random
from enum import Enum

from task50.marusya.utils.Board import Board
from task50.marusya.utils.Vector2 import Vector2


class State(Enum):
    WIN = 1
    IN_PROGRESS = 0
    FAIL = -1


class Game:
    def __init__(self):
        self.MAX = 2048
        self.MAX_LEN = len(str(self.MAX))
        self.w = 4
        self.h = 4
        self.ROW_SEPARATOR = '\n' + ''"-" * (self.w * (self.MAX_LEN + 1)) + '\n'
        self.board = Board(self.h, self.w)
        self.score = 0
        self.accepted_moves = {'l': ['u', 'd', 'l', 'r'],
                               'r': ['u', 'd', 'l', 'r'],
                               'u': ['u', 'd', 'l', 'r'],
                               'd': ['u', 'd', 'l', 'r']}
        self.state = State.IN_PROGRESS
        self.step()
        self.step()

    def get_state(self):
        draw_board = list()
        for row in range(self.h):
            draw_row = list()
            for col in range(self.w):
                cell = Vector2(col, row)
                value = self.board.get(cell)
                if value == 0:
                    draw_row.append('.' * self.MAX_LEN)
                else:
                    draw_row.append(("." * (self.MAX_LEN - len(str(value)))) + str(value))
            draw_board.append('|'.join(draw_row))
        return self.ROW_SEPARATOR.join(draw_board)

    def move(self, direction):
        if direction == "l":
            self.board.move_l()
        elif direction == "r":
            self.board.move_r()
        elif direction == "u":
            self.board.move_u()
        else:
            self.board.move_d()
        check_res = self.check()
        if self.state == State.IN_PROGRESS:
            self.step()
        self.count_score()

    def step(self):
        cells = []
        for i in range(self.w):
            for j in range(self.h):
                cell = Vector2(j, i)
                value = self.board.get(cell)
                if value == 0:
                    cells.append(cell)
        random.shuffle(cells)
        print(cells[0])
        if random.random() < 0.9:
            self.board.set(cells[0], 2)
        else:
            self.board.set(cells[0], 4)

    def check(self):
        self.state = State.FAIL
        for i in range(self.w):
            for j in range(self.h):
                cell = Vector2(j, i)
                value = self.board.get(cell)
                self.score += value
                if value == 2048:
                    self.state = State.WIN
                if value == 0 and self.state != State.WIN:
                    self.state = State.IN_PROGRESS

    def count_score(self):
        self.score = 0
        for i in range(self.w):
            for j in range(self.h):
                value = self.board.get(Vector2(j, i))
                self.score += value
