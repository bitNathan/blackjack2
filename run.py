import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description="deploy or test Blackjack2")
    parser.add_argument("command", nargs="?", help="\"test\", \"flask\", or \"play\"")
    args = parser.parse_args()

    if (args.command is None or args.command == "flask"):
        run_flask()
    elif args.command == "test":
        run_tests()
    elif args.command == "play":
        run_cli_game()


def run_cli_game():
    CliGame.play_game()


def run_flask():
    os.execvp("flask", ["flask", "run"])


def run_tests():
    env = os.environ.copy()
    env['PYTHONPATH'] = '.'  # same as PYTHONPATH=. in the shell

    cmd = ['pytest', '--cov=app']
    result = subprocess.run(cmd, env=env)
    sys.exit(result.returncode)


class CliGame:

    @staticmethod
    def play_game():
        from app.game.blackjack import BlackjackGame
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

if __name__ == "__main__":
    main()
