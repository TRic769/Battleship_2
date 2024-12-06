from typing import Optional, Tuple
from .board import Board
from .player import AIPlayer
from .ship import Ship
from .enums import GamePhase
from ..constants import SHIPS
from ..ui.console_ui import ConsoleUI

class GameState:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.ai_player = AIPlayer()
        self.ui = ConsoleUI()
        self.current_phase = GamePhase.SETUP
        self.winner = None

    def run(self):
        """Main game loop"""
        self.setup_game()
        
        while self.current_phase == GamePhase.PLAYING:
            # Display game state
            self.ui.display_boards(self.player_board, self.computer_board)
            
            # Player's turn
            hit, message = self.player_turn()
            if message:
                self.ui.show_message(message)
            if self.current_phase == GamePhase.GAME_OVER:
                break
                
            # Computer's turn
            hit, message = self.computer_turn()
            if message:
                self.ui.show_message(message)
                
        self.ui.show_game_over(self.winner)

    def setup_game(self):
        """Handle game setup phase"""
        # Player ship placement
        for ship_name, length in SHIPS.items():
            self.ui.display_boards(self.player_board, self.computer_board)
            while True:
                coordinates = self.ui.get_ship_placement(ship_name, length)
                ship = Ship(ship_name, length, coordinates)
                if self.player_board.place_ship(ship):
                    break
                self.ui.show_message("Invalid placement! Try again.")

        # Computer ship placement (random)
        self._setup_computer_ships()
        self.current_phase = GamePhase.PLAYING

    def player_turn(self) -> Tuple[bool, Optional[str]]:
        """Handle player's turn"""
        while True:
            x, y = self.ui.get_shot_input()
            if (x, y) not in self.computer_board.shots:
                break
            self.ui.show_message("You already shot there! Try again.")

        hit = self.computer_board.receive_shot(x, y)
        if hit:
            message = "Hit!"
            if self.computer_board.all_ships_sunk():
                self.current_phase = GamePhase.GAME_OVER
                self.winner = "Player"
                return True, "You win!"
        else:
            message = "Miss!"
        return hit, message

    def computer_turn(self) -> Tuple[bool, Optional[str]]:
        """Handle computer's turn"""
        x, y = self.ai_player.get_shot(self.player_board)
        hit = self.player_board.receive_shot(x, y)
        self.ai_player.process_shot_result(x, y, hit)
        
        if hit:
            message = "Computer hit your ship!"
            if self.player_board.all_ships_sunk():
                self.current_phase = GamePhase.GAME_OVER
                self.winner = "Computer"
                return True, "Computer wins!"
        else:
            message = "Computer missed!"
        return hit, message

    def _setup_computer_ships(self):
        """Place computer ships randomly"""
        from random import choice
        for ship_name, length in SHIPS.items():
            while True:
                # Get all valid placements for this ship
                valid_placements = self.computer_board.get_valid_ship_placements(length)
                if not valid_placements:
                    continue
                    
                # Choose a random valid placement
                coordinates = choice(valid_placements)
                ship = Ship(ship_name, length, coordinates)
                if self.computer_board.place_ship(ship):
                    break
