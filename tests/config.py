from app.services.game_service import GameService
from app.game.blackjack import BlackjackGame
from app.api.routes import api_bp

from tests.doubles.dummy_game_class import DummyGameClass


class ServiceTestingConfig():
    DEBUG = True
    GAME_CLASS = DummyGameClass
    GAME_SERVICE = GameService(GAME_CLASS)


class GameClassTestingConfig():
    DEBUG = True
    GAME_CLASS = BlackjackGame


class apiClassTestConfig():
    DEBUG = True
    ROUTE_CLASS = api_bp
    GAME_CLASS = BlackjackGame
    GAME_SERVICE = GameService(GAME_CLASS)
