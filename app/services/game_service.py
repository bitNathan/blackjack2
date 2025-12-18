from flask import Response


class GameService():
    def __init__(self, game_cls):
        self.games = dict()
        # will usually be BlackjackGame, but mocked for testing
        self.game_cls = game_cls

    def _formatStatus(self, game_id, game):
        status = game.status()

        # hiding dealer cards before game is over
        dealer_cards = status["dealer_hand"]
        if (len(dealer_cards) >= 1 and status["game_state"] != "resolved"):
            dealer_cards = dealer_cards[0]

        return {
            "id": game_id,
            "hand": status["player_hand"],
            "value": status["player_value"],
            "dealer_hand": dealer_cards,
            "game_state": status["game_state"],
            "winner": status["winner"]
        }

    # TODO handle custom errors, like actions on wrong game states
    def get_all_games(self):
        # TODO should get status of each?
        return list(self.games.keys())

    def start_new_game(self):
        game = self.game_cls()
        game_id = len(self.games)
        self.games[game_id] = game
        return self._formatStatus(game_id, game)

    def deal(self, id):
        game = self.games[id]
        assert game.game_state == "new"
        game.start_game()
        return self._formatStatus(id, game)

    def get_game(self, id):
        if (id not in self.games):
            raise ValueError("Invalid game id")
        return self._formatStatus(id, self.games[id])

    def hit(self, id):
        game = self.games[id]
        # TODO import game states from game, not raw strings
        assert game.game_state == "in_play"
        game.hit()
        return self._formatStatus(id, game)

    def stand(self, id):
        game = self.games[id]
        assert game.game_state == "in_play"
        if (game.game_over):
            raise ValueError("Game is finished, cannot hit")
        game.stand()
        return self._formatStatus(id, game)

    def reset_game(self, id):
        if (id not in self.games):
            raise ValueError("Expected existing game id")
        self.games[id] = self.game_cls()
        return self._formatStatus(id, self.games[id])

    def delete_game(self, id):
        if (id not in self.games):
            raise ValueError("Expected existing game id")
        self.games.pop(id)
        return Response(status=204)
