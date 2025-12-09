from .services import GameService
from .game import BlackjackGame


class DevelopmentConfig():
    DEBUG = True
    GAME_CLASS = BlackjackGame
    GAME_SERVICE = GameService(GAME_CLASS)
