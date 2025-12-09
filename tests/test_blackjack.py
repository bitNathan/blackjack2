from app.game import Card
import random
import pytest


def test_game_initial_deal(game_class_test_class):
    game = game_class_test_class()
    game.start_game()

    assert len(game.player.hands[0].cards) == 2
    assert len(game.dealer.hands[0].cards) == 2
    assert not game.game_over


def test_player_busts(game_class_test_class):
    game = game_class_test_class()
    game.start_game()
    game.game_over = True  # simulate finished game

    with pytest.raises(AssertionError):
        game.hit()


def test_hit_then_bust(game_class_test_class):
    game = game_class_test_class()
    game.start_game()

    hand = game.player.hands[0]
    hand.cards = []  # clear and rig the hand to bust
    hand.add_card(game.deck.draw())
    hand.add_card(game.deck.draw())
    hand.add_card(game.deck.draw())
    hand.add_card(game.deck.draw())

    if hand.value() > 21:
        # with pytest.raises(AssertionError):
        game.stand()
        response = game.status()
        assert response["game_state"] == "resolved"
        assert game.game_over
        assert game.winner == 'dealer'


def test_stand_dealer_wins(game_class_test_class, monkeypatch):
    game = game_class_test_class()
    game.start_game()

    player_hand = game.player.hands[0]
    dealer_hand = game.dealer.hands[0]

    player_hand.cards = []
    dealer_hand.cards = []

    test_cards = [
        Card('10', 'Hearts'), Card('8', 'Spades'),   # dealer deal
        Card('2', 'Hearts'),    # dealer hit
        Card('10', 'Clubs'), Card('6', 'Diamonds'),  # plaeyr  deaalt
        Card('8', 'Clubs')  # player busts
    ]
    monkeypatch.setattr(game.deck, 'draw', lambda: test_cards.pop(0))

    dealer_hand.add_card(game.deck.draw())
    dealer_hand.add_card(game.deck.draw())
    dealer_hand.add_card(game.deck.draw())

    player_hand.add_card(game.deck.draw())
    player_hand.add_card(game.deck.draw())
    player_hand.add_card(game.deck.draw())

    game._dealer_turn = lambda: None

    response = game.stand()
    assert "dealer_hand" in response
    assert "player_hand" in response
    assert "player_value" in response
    assert game.game_over
    assert game.winner == 'dealer'


def test_stand_player_wins(game_class_test_class, monkeypatch):
    game = game_class_test_class()
    game.start_game()

    player_hand = game.player.hands[0]
    dealer_hand = game.dealer.hands[0]

    player_hand.cards = []
    dealer_hand.cards = []

    test_cards = [
        Card('10', 'Hearts'), Card('8', 'Spades'),   # player deal
        Card('2', 'Hearts'),    # player hit
        Card('10', 'Clubs'), Card('6', 'Diamonds'),  # dealer deaalt
        Card('8', 'Clubs')  # dealer busts
    ]
    monkeypatch.setattr(game.deck, 'draw', lambda: test_cards.pop(0))

    player_hand.add_card(game.deck.draw())
    player_hand.add_card(game.deck.draw())
    player_hand.add_card(game.deck.draw())

    dealer_hand.add_card(game.deck.draw())
    dealer_hand.add_card(game.deck.draw())
    dealer_hand.add_card(game.deck.draw())

    game._dealer_turn = lambda: None

    game.stand()
    assert game.winner == 'player'


def test_stand_push(game_class_test_class, monkeypatch):
    game = game_class_test_class()
    game.start_game()

    player_hand = game.player.hands[0]
    dealer_hand = game.dealer.hands[0]

    player_hand.cards = []
    dealer_hand.cards = []

    test_cards = [
        Card('10', 'Hearts'), Card('8', 'Spades'),   # player deal
        Card('8', 'Clubs'), Card('10', 'Diamonds'),  # dealer deaalt
    ]
    monkeypatch.setattr(game.deck, 'draw', lambda: test_cards.pop(0))

    player_hand.add_card(game.deck.draw())
    player_hand.add_card(game.deck.draw())

    dealer_hand.add_card(game.deck.draw())
    dealer_hand.add_card(game.deck.draw())

    game._dealer_turn = lambda: None

    game.stand()
    assert game.winner == 'push'


def test_stand_when_game_over(game_class_test_class):
    game = game_class_test_class()
    game.start_game()
    game.game_over = True

    with pytest.raises(AssertionError):
        game.stand()


def test_random_games_playthrough(game_class_test_class):
    for _ in range(10):
        game = game_class_test_class()
        game.start_game()

        assert len(game.player.hands[0].cards) == 2
        assert len(game.dealer.hands[0].cards) == 2

        # Simulate player's turn
        while not game.game_over:
            action = random.choice(['hit', 'stand'])
            if action == 'hit':
                result = game.hit()
                if "Game already over" in result:
                    break  # game ended from bust
            else:
                result = game.stand()
                break  # always end after stand

        # Validate final state
        assert game.game_over
        assert game.winner in ('player', 'dealer', 'push')

        status = game.status()
        assert isinstance(status['player_hand'], list)
        assert isinstance(status['dealer_hand'], list)
        assert isinstance(status['player_value'], int)
        assert isinstance(status['dealer_value'], int)


def test_status_returns_expected_keys(game_class_test_class):
    game = game_class_test_class()
    game.start_game()
    status = game.status()

    assert 'player_hand' in status
    assert 'dealer_hand' in status
    assert 'player_value' in status
    assert 'dealer_value' in status
    assert 'winner' in status
