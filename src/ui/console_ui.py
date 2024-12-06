from typing import Tuple, List
from ..constants import BOARD_SIZE, WATER, SHIP, HIT, MISS
from ..game.board import Board
from ..game.enums import GamePhase

class ConsoleUI:
    @staticmethod
    def display_boards(player_board: Board, computer_board: Board):
        """Display both game boards side by side"""
        print("\n  Your Board          Computer's Board")
        print("  0123456789          0123456789")
        
        for y in range(BOARD_SIZE):
            # Player's board
            print(f"{y} ", end="")
            for x in range(BOARD_SIZE):
                print(player_board.grid[y][x], end="")
            
            # Separator
            print("        ", end="")
            
            # Computer's board (hiding ships)
            print(f"{y} ", end="")
            for x in range(BOARD_SIZE):
                cell = computer_board.grid[y][x]
                if cell == SHIP:  # Hide computer's ships
                    print(WATER, end="")
                else:
                    print(cell, end="")
            print()

    @staticmethod
    def get_shot_input() -> Tuple[int, int]:
        """Get shot coordinates from the player"""
        while True:
            try:
                move = input("\nEnter your shot (row,col): ")
                y, x = map(int, move.split(','))
                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                    return x, y
                print(f"Coordinates must be between 0 and {BOARD_SIZE-1}")
            except ValueError:
                print("Invalid input. Please enter row,col (e.g., 3,4)")

    @staticmethod
    def get_ship_placement(ship_name: str, length: int) -> List[Tuple[int, int]]:
        """Get ship placement coordinates from the player"""
        print(f"\nPlacing {ship_name} (length: {length})")
        while True:
            try:
                start = input("Enter start position (row,col): ")
                direction = input("Enter direction (h/v): ").lower()
                
                start_y, start_x = map(int, start.split(','))
                coordinates = []
                
                if direction == 'h':
                    if start_x + length > BOARD_SIZE:
                        print("Ship would be out of bounds!")
                        continue
                    coordinates = [(start_x + i, start_y) for i in range(length)]
                elif direction == 'v':
                    if start_y + length > BOARD_SIZE:
                        print("Ship would be out of bounds!")
                        continue
                    coordinates = [(start_x, start_y + i) for i in range(length)]
                else:
                    print("Invalid direction! Use 'h' for horizontal or 'v' for vertical")
                    continue
                
                return coordinates
                
            except ValueError:
                print("Invalid input. Please enter coordinates as row,col (e.g., 3,4)")

    @staticmethod
    def show_message(message: str):
        """Display a game message"""
        print(f"\n{message}")

    @staticmethod
    def show_game_over(winner: str):
        """Display game over message"""
        print("\n" + "="*40)
        print(f"Game Over! {winner} wins!")
        print("="*40)
