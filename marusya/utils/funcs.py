from . import cards
from random import choice


def get_ai_score():
    score = 0
    while score < 16:
        score += choice(list(cards.values()))
    return score
