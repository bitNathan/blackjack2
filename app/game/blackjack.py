# blackjack.py

from .deck import Deck
from .player import Player
from .dealer import Dealer
from .hand import Hand

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
        self.active_hand_index = 0  # track which hand the player is playing
        self.game_over = False
        self.winner = None  # could be 'player', 'dealer', 'push'

    def start_game(self):
        """Deals two cards to player and dealer (dealer gets one face down)"""
        self.deck.shuffle()
        for _ in range(2):
            self.player.hands[0].add_card(self.deck.draw())

        # Deal to dealer
        for _ in range(2):
            self.dealer.hands[0].add_card(self.deck.draw())

    def current_hand(self):
        return self.player.hands[self.active_hand_index]

    def hit(self):
        """Player requests another card"""
        if self.game_over:
            return "Game already over"

        hand = self.current_hand()
        hand.add_card(self.deck.draw())

        if hand.is_busted():
            self.game_over = True
            self.winner = 'dealer'
            return "Player busts! Dealer wins."

        return f"Player hits. Hand value: {hand.value()}"

    def stand(self):
        """Player ends turn, dealer plays"""
        if self.game_over:
            return "Game already over"

        self._dealer_turn()
        self._resolve_game()
        return self.status()

    def _dealer_turn(self):
        """Dealer hits until reaching 17+"""
        hand = self.dealer.hands[0]
        while hand.value() < 17:
            hand.add_card(self.deck.draw())

    def _resolve_game(self):
        """Compare hands and determine winner"""
        self.game_over = True
        player_val = self.current_hand().value()
        dealer_val = self.dealer.hands[0].value()

        if self.current_hand().is_busted():
            self.winner = 'dealer' # player busted
        elif self.dealer.hands[0].is_busted():
            self.winner = 'player'
        elif player_val > dealer_val:
            self.winner = 'player'
        elif dealer_val > player_val:
            self.winner = 'dealer'
        else:
            self.winner = 'push'

    def status(self):
        """Returns a summary of game state"""
        return {
            'player_hand': [f"{c.rank} of {c.suit}" for c in self.current_hand().cards],
            'player_value': self.current_hand().value(),
            'dealer_hand': [f"{c.rank} of {c.suit}" for c in self.dealer.hands[0].cards],
            'dealer_value': self.dealer.hands[0].value(),
            'winner': self.winner if self.game_over else None
        }

