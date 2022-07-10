from task50.marusya.utils.Vector2 import Vector2


class Board:
    def __init__(self, height: int, width: int):
        self.width = width
        self.height = height
        self.array = [[0 for i in range(width)] for j in range(height)]

    def get(self, vec: Vector2):
        if 0 <= vec.y < self.height and 0 <= vec.x < self.width:
            return self.array[vec.y][vec.x]
        return None

    def set(self, vec: Vector2, value: int):
        self.array[vec.y][vec.x] = value

    def move(self, direction: Vector2, start: list):
        for c in start:
            tmp = c
            while self.get(c) is not None:
                cur = c
                while cur != tmp and self.try_move(cur, cur - direction):
                    cur = cur - direction
                c = c + direction

    def move_r(self):
        self.move(Vector2(-1, 0), [Vector2(self.width - 1, i) for i in range(self.height)])

    def move_l(self):
        self.move(Vector2(1, 0), [Vector2(0, i) for i in range(self.height)])

    def move_d(self):
        self.move(Vector2(0, -1), [Vector2(i, self.height - 1) for i in range(self.width)])

    def move_u(self):
        self.move(Vector2(0, 1), [Vector2(i, 0) for i in range(self.width)])

    def try_move(self, a: Vector2, b: Vector2) -> bool:
        if self.get(a) == self.get(b):
            self.set(a, 0)
            self.set(b, self.get(b) * 2)
            return False
        if self.get(a) == 0:
            return True
        if self.get(b) == 0:
            self.set(b, self.get(a))
            self.set(a, 0)
            return True
        return False
