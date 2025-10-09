# hand.py
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        total = 0
        aces = 0
        for card in self.cards:
            val = card.value()
            total += val
            if card.rank == 'A':
                aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_busted(self):
        return self.value() > 21

    def is_blackjack(self):
        return self.value() == 21 and len(self.cards) == 2

