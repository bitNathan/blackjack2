# app/game/cli.py
from .blackjack import BlackjackGame

game = BlackjackGame()
game.start_game()

while not game.game_over:
    print(game.status())
    move = input("Hit or stand? ").lower()
    if move == 'hit':
        print(game.hit())
    elif move == 'stand':
        print(game.stand())
    else:
        print("Invalid move")

print("\nGame Over!")
print(game.status())

