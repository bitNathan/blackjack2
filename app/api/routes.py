from flask import Blueprint, current_app
# from ..services.game_service import *

api_bp = Blueprint("api", __name__)


@api_bp.get("/")
def get_games():
    gameService = current_app.config['GAME_SERVICE']
    return gameService.get_all_games()


@api_bp.post("/games")
def post_new_game():
    gameService = current_app.config['GAME_SERVICE']
    return gameService.start_new_game()


@api_bp.get("/games/<int:id>")
def get_game_status(id: int):
    gameService = current_app.config['GAME_SERVICE']
    return gameService.get_game(id)


@api_bp.post("/games/<int:id>/reset")
def reset_game(id):
    gameService = current_app.config['GAME_SERVICE']
    return gameService.reset_game(id)


@api_bp.post("/games/<int:id>/deal")
def deal(id):
    gameService = current_app.config['GAME_SERVICE']
    return gameService.deal(id)


@api_bp.post("/games/<int:id>/<action>")
def perform_game_action(id, action):
    gameService = current_app.config['GAME_SERVICE']
    if (action not in ["hit", "stand"]):
        raise ValueError("Expected action to be \"hit\" or \"stand\"")
    if (action == "hit"):
        return gameService.hit(id)
    return gameService.stand(id)


@api_bp.delete("games/<int:id>")
def delete_game(id):
    gameService = current_app.config['GAME_SERVICE']
    return gameService.delete_game(id)
