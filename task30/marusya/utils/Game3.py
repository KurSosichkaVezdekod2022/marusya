from random import choice
from copy import deepcopy


class Board:
    def __init__(self):
        self.h = 10
        self.w = 10
        self.board = self.create_new_board()

        self.empty = '*'
        self.tile = '#'

        self.shapes = {"I": [[1], [1], [1], [1]],
                       "L": [[1, 0], [1, 0], [1, 1]],
                       "J": [[0, 1], [0, 1], [1, 1]],
                       "O": [[1, 1], [1, 1]],
                       "T": [[0, 1, 0], [1, 1, 1]],
                       "S": [[0, 1, 1], [1, 1, 0]],
                       "Z": [[1, 1, 0], [0, 1, 1]]}

        self.current_block_position = None
        self.current_block = None
        self.next_block = None

        self.game_running = True
        self.score = 0

    def start_game(self):
        self.board = self.create_new_board()
        self.current_block_position = None
        self.current_block = None
        self.next_block = None
        self.game_running = True
        self.score = 0
        self.put_new_block()

    def put_new_block(self):
        if self.current_block is None:
            self.current_block = self.get_block()
        else:
            self.current_block = self.next_block
        self.next_block = self.get_block()
        self.current_block_position = [0, 4]
        if self.check_collisions(self.current_block_position, self.current_block.shape):
            print("end game")
            self.game_running = False
        else:
            self.score += 5

    def rotate_block(self):
        rot_sh = list(map(list, zip(*self.current_block.shape[::-1])))
        if self.can_move(self.current_block_position, rot_sh):
            self.current_block.shape = rot_sh
        self.move(3)

    def move(self, direction):
        pos = self.current_block_position
        new_pos = [0, 0]
        d = False
        if direction == 1:  # l
            new_pos = [pos[0], pos[1] - 1]
        elif direction == 2:  # r
            new_pos = [pos[0], pos[1] + 1]
        elif direction == 3:  # d
            new_pos = [pos[0] + 1, pos[1]]
            d = True
        if self.can_move(new_pos, self.current_block.shape):
            print("can")
            self.current_block_position = new_pos
            if not d:
                self.move(3)
        elif direction == 3:
            self.land_block()
            self.rows_destroy()
            self.put_new_block()

    def check_collisions(self, pos, shape):
        size = [len(shape), len(shape[0])]
        for y in range(size[0]):
            for x in range(size[1]):
                if shape[y][x] == 1 and self.board[pos[0] + y][pos[1] + x] == 1:
                    return True

    def can_move(self, pos, shape):
        size = [len(shape), len(shape[0])]
        if pos[1] < 0 or pos[1] + size[1] > self.w or pos[0] + size[0] > self.h:
            return False
        return not self.check_collisions(pos, shape)

    def land_block(self):
        shape = self.current_block.shape
        pos = self.current_block_position
        size = self.current_block.size
        for y in range(size[0]):
            for x in range(size[1]):
                if shape[y][x] == 1:
                    self.board[pos[0] + y][pos[1] + x] = 1

    def get_block(self):
        block = Block(choice(list(self.shapes.values())))
        if choice([False, True]):
            block.flip()
        return block

    def is_game_running(self):
        return self.game_running

    def create_new_board(self):
        return [[0 for _ in range(self.w)] for _ in range(self.h)]

    def get_state(self):
        print_board = list()
        board = deepcopy(self.board)
        shape = self.current_block.shape
        size = self.current_block.size
        pos = self.current_block_position
        for y in range(size[0]):
            for x in range(size[1]):
                if shape[y][x] == 1:
                    board[pos[0] + y][pos[1] + x] = 1
        for row in range(self.h):
            print_row = list()
            for col in range(self.w):
                if board[row][col] == 1:
                    print_row.append(self.tile)
                else:
                    print_row.append(self.empty)
            print_board.append(' '.join(print_row))
        return '\n'.join(print_board)

    def rows_destroy(self):
        for row in range(self.h):
            if all(col != 0 for col in self.board[row]):
                for r in range(row, 0, -1):
                    self.board[r] = self.board[r - 1]
                self.board[0] = [0 for _ in range(self.w)]
                self.score += 100


class Block:
    def __init__(self, shape):
        self.shape = shape

    def flip(self):
        self.shape = list(map(list, self.shape[::-1]))

    @property
    def size(self):
        return [len(self.shape), len(self.shape[0])]
