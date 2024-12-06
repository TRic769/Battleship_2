from .game.game_state import GameState

def main():
    game = GameState(use_gui=True)
    game.run()

if __name__ == "__main__":
    main() 