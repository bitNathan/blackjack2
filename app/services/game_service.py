from flask import Response


class GameService():
    def __init__(self, game_cls):
        self.games = dict()
        # will usually be BlackjackGame, but mocked for testing
        self.game_cls = game_cls

    # TODO handle custom errors, like actions on wrong game states
    def get_all_games(self):
        # TODO should get status of each?
        return list(self.games.keys())

    def start_new_game(self):
        game = self.game_cls()
        game_id = len(self.games)
        self.games[game_id] = game
        status = game.status()
        return {
            "id": game_id,
            "hand": status["player_hand"],
            "value": status["player_value"],
            "game_state": status["game_state"],
            "winner": status["winner"]
        }

    def deal(self, id):
        game = self.games[id]
        assert game.game_state == "new"
        game.start_game()
        status = game.status()
        return {
            "hand": status["player_hand"],
            "value": status["player_value"],
            "game_state": status["game_state"],
            "winner": status["winner"]
        }

    def get_game(self, id):
        if (id not in self.games):
            raise ValueError("Invalid game id")
        status = self.games[id].status()
        return {
            "id": id,
            "hand": status["player_hand"],
            "value": status["player_value"],
            "game_state": status["game_state"],
            "winner": status["winner"]
        }

    def hit(self, id):
        game = self.games[id]
        # TODO import game states from game, not raw strings
        assert game.game_state == "in_play"
        game.hit()
        status = game.status()
        return {
            "hand": status["player_hand"],
            "value": status["player_value"],
            "game_state": status["game_state"],
            "winner": status["winner"]
        }

    def stand(self, id):
        game = self.games[id]
        assert game.game_state == "in_play"
        if (game.game_over):
            raise ValueError("Game is finished, cannot hit")
        game.stand()
        status = game.status()
        return {
            "hand": status["player_hand"],
            "value": status["player_value"],
            "game_state": status["game_state"],
            "winner": status["winner"]
        }

    def reset_game(self, id):
        if (id not in self.games):
            raise ValueError("Expected existing game id")
        self.games[id] = self.game_cls()
        status = self.games[id].status()
        return {
            "hand": status["player_hand"],
            "value": status["player_value"],
            "game_state": status["game_state"],
            "winner": status["winner"]
        }

    def delete_game(self, id):
        if (id not in self.games):
            raise ValueError("Expected existing game id")
        self.games.pop(id)
        return Response(status=204)
