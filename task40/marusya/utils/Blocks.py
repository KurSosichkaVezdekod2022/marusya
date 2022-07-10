from random import choice
from

class Block:
    def __init__(self):

    def rotate(self):
        next_brick = list(zip(*self.shape))[::-1]
        return next_brick

    def move(self):
