def test_empty_get_all_games_route(client):
    response = client.get("/api/")

    assert response.status_code == 200, f"Expected 200, got {response}"
    data = response.get_json()
    assert data == [], "Expected list of games to be empty"


def test_non_empty_get_all_games_route(client):
    client.post("/api/games")
    response = client.get("/api/")

    assert response.status_code == 200, f"Expected 200, got {response}"
    data = response.get_json()
    assert len(data) == 1, "Expected list to contain 1 game"
    assert data[0] == 0, "Expected game id to be 0"


def test_get_game_by_id(client):
    client.post("/api/games")
    client.post("/api/games")
    client.post("/api/games")
    response = client.get("/api/games/1")

    assert response.status_code == 200, f"Expected 200, got {response}"
    data = response.get_json()
    assert data["game_state"] == "new"
    assert data["id"] == 1


def test_game_reset(client):
    client.post("/api/games")
    client.post("/api/games")
    client.post("/api/games/1/deal")
    response = client.get("/api/games/1")

    assert response.status_code == 200, f"Expected 200, got {response}"
    data = response.get_json()
    assert data["game_state"] == "in_play"
    assert data["id"] == 1

    client.post("/api/games/1/reset")
    response = client.get("/api/games/1")
    data = response.get_json()
    assert data["game_state"] == "new"
    assert data["id"] == 1


def test_deal(client):
    client.post("/api/games")
    client.post("/api/games")
    client.post("/api/games/1/deal")
    response = client.get("/api/games/1")

    assert response.status_code == 200, f"Expected 200, got {response}"
    data = response.get_json()
    assert data["game_state"] == "in_play"
    assert data["id"] == 1
    assert len(data["hand"]) == 2, f"Expected 2 cards in hand, got {response}"


def test_hit_and_stand(client):
    client.post("/api/games")
    client.post("/api/games")

    for i in range(10):
        client.post("/api/games/0/deal")
        client.post("/api/games/0/hit")

        response = client.get("/api/games/0")
        if (response.get_json()["game_state"] == "in_play"):
            client.post("/api/games/0/stand")

        response = client.get("/api/games/0")

        assert response.status_code == 200, f"Expected 200, got {response}"
        data = response.get_json()
        assert data["game_state"] == "resolved", \
            f"expected state to be resolved, got {data["game_state"]}"

        assert data["id"] == 0
        assert len(data["hand"]) == 3, \
            f"Expected 3 cards in hand, got {len(data["hand"])}"
        assert data["winner"] is not None, "winner is not null"
        client.post("/api/games/0/reset")


def test_delete(client):
    client.post("/api/games")
    response = client.get("/api/")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

    client.delete("/api/games/0")
    response = client.get("/api/")
    assert response.status_code == 200
    assert len(response.get_json()) == 0
