# dealer.py
from .player import Player

class Dealer(Player):
    def play(self, deck):
        hand = self.hands[0]
        while hand.value() < 17:
            hand.add_card(deck.deal())
