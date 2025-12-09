import pytest


def test_get_all_games_empty(service_game_service):
    result = service_game_service.get_all_games()
    assert result == [], "Expected to find empty list of no games"


def test_create_and_get_all_games(service_game_service):
    NUM_GAMES = 10
    for i in range(NUM_GAMES):
        service_game_service.start_new_game()

    result = service_game_service.get_all_games()
    assert len(result) == NUM_GAMES, \
        f"Expected to find list of {NUM_GAMES} games"


def test_deal(service_game_service):
    service_game_service.start_new_game()
    response = service_game_service.deal(0)
    assert "hand" in response
    assert "value" in response
    assert "game_state" in response
    assert "winner" in response


def _delete_all_games(service_game_service):
    game_ids = service_game_service.get_all_games()

    for id in game_ids:
        service_game_service.delete_game(id)


def test_get_game_by_id(service_game_service):

    _delete_all_games(service_game_service)  # tested in seperate function
    # add new games and get statuses
    NUM_GAMES = 10
    for i in range(NUM_GAMES):
        service_game_service.start_new_game()
    for i in range(NUM_GAMES):
        service_game_service.get_game(i)

    with pytest.raises(ValueError):
        service_game_service.get_game(NUM_GAMES)


def test_delete_game(service_game_service):
    NUM_GAMES = 10
    for i in range(NUM_GAMES):
        service_game_service.start_new_game()
    _delete_all_games(service_game_service)
    assert len(service_game_service.get_all_games()) == 0


def test_hit_increments(service_game_service):
    # dummy game class just increments counter on hit / stand
    # returns counter under player_hand -> hand
    game_id = service_game_service.start_new_game()["id"]
    service_game_service.deal(game_id)

    NUM_HITS = 9
    for i in range(NUM_HITS):
        service_game_service.hit(game_id)

    response = service_game_service.get_game(game_id)
    assert response["hand"] == NUM_HITS, f"{response}"


def test_stand_increments(service_game_service):
    # dummy game class just increments counter on hit / stand
    # returns counter under player_value -> value
    game_id = service_game_service.start_new_game()["id"]
    service_game_service.deal(game_id)
    service_game_service.stand(game_id)

    with pytest.raises(AssertionError):
        service_game_service.stand(game_id)

    response = service_game_service.get_game(game_id)
    assert response["value"] == 1, f"{response}"


def test_no_hit_after_stand(service_game_service):
    game_id = service_game_service.start_new_game()["id"]
    service_game_service.deal(game_id)
    service_game_service.stand(game_id)

    with pytest.raises(AssertionError):
        service_game_service.hit(game_id)


def test_game_reset(service_game_service):
    game_id = service_game_service.start_new_game()["id"]
    service_game_service.deal(game_id)

    service_game_service.hit(game_id)
    service_game_service.hit(game_id)
    service_game_service.hit(game_id)
    service_game_service.hit(game_id)

    response = service_game_service.get_game(game_id)
    assert response["hand"] == 4, f"{response}"

    service_game_service.reset_game(game_id)

    response = service_game_service.get_game(game_id)
    assert response["hand"] == 0, f"{response}"
