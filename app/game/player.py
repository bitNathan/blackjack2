# player.py
from .hand import Hand


class Player:
    def __init__(self):
        self.hands = [Hand()]  # TODO suport up to three hands per player
