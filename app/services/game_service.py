from ..game import *

class GameService():
    games = dict()

    # TODO all functions should only return "visible" information
    
    def get_all_games(self):
        # TODO should get status of each?
        return list(self.games.keys())

    def start_new_game(self):
        game = BlackjackGame()
        game_id = len(self.games)
        self.games[game_id] = game
        return [game.status(), game_id]
    
    def deal(self, id):
        self.games[id].start_game()
        return self.games[id].status()

    def get_game(self, id):
        if (id in self.games):
            return self.games[id].status()
        else:
            raise ValueError("Invalid game id")

    # TODO hit and stand should only work if we've dealt already
    def hit(self, id):
        game = self.games[id]
        if (game.game_over):
            raise ValueError("Game is finished, cannot hit")
        return self.games[id].hit()

    def stand(self,id):
        game = self.games[id]
        if (game.game_over):
            raise ValueError("Game is finished, cannot hit")
        return game.stand()

    def reset_game(self, id):
        if (id not in self.games):
            raise ValueError("Expected existing game id")
        self.games[id] = BlackjackGame()
        return self.games[id].status()

    def delete_game(self, id):
        if (id not in self.games):
            raise ValueError("Expected existing game id")
        self.games.pop(id)

