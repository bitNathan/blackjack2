
class DummyGameClass:
    def __init__(self):
        self.game_state = "new"
        self.num_hits = 0
        self.num_stands = 0
        self.game_over = False

    def start_game(self):
        assert self.game_state == "new"
        self.game_state = "in_play"

    def hit(self):
        assert self.game_state == "in_play"
        self.num_hits += 1

    def stand(self):
        assert self.game_state == "in_play"
        self.game_over = True
        self.game_state = "resolved"
        self.num_stands += 1

    def status(self):
        return {
            "id": -1,
            "player_hand": self.num_hits,
            "player_value": self.num_stands,
            "game_state": "game_state",
            "winner": "winner"
        }
