class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __invert__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + (other.__invert__())
