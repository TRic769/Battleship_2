from typing import List, Tuple
from .ship import Ship
from ..constants import BOARD_SIZE, EMPTY, SHIP, MISS, HIT, WATER

class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.ships: List[Ship] = []
        self.shots: List[Tuple[int, int]] = []

    def place_ship(self, ship: Ship) -> bool:
        """Attempt to place a ship on the board"""
        for x, y in ship.coordinates:
            if not self._is_valid_position(x, y) or self.grid[y][x] != EMPTY:
                return False
        
        for x, y in ship.coordinates:
            self.grid[y][x] = SHIP
        self.ships.append(ship)
        return True

    def receive_shot(self, x: int, y: int) -> bool:
        """Process a shot at the given coordinates"""
        if not self._is_valid_position(x, y) or (x, y) in self.shots:
            return False

        self.shots.append((x, y))
        
        if self.grid[y][x] == SHIP:
            self.grid[y][x] = HIT
            for ship in self.ships:
                if ship.hit((x, y)):
                    break
            return True
        
        self.grid[y][x] = MISS
        return False

    def _is_valid_position(self, x: int, y: int) -> bool:
        """Check if the given coordinates are within bounds"""
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

    def all_ships_sunk(self) -> bool:
        """Check if all ships have been sunk"""
        return all(ship.is_sunk for ship in self.ships)

    def get_valid_ship_placements(self, length: int) -> List[List[Tuple[int, int]]]:
        """Returns all valid ship placements for a ship of given length."""
        valid_placements = []
        
        # Check horizontal placements
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE - length + 1):
                coordinates = [(x + i, y) for i in range(length)]
                if all(self._is_valid_position(x, y) and 
                      self.grid[y][x] == EMPTY for x, y in coordinates):
                    valid_placements.append(coordinates)
        
        # Check vertical placements
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE - length + 1):
                coordinates = [(x, y + i) for i in range(length)]
                if all(self._is_valid_position(x, y) and 
                      self.grid[y][x] == EMPTY for x, y in coordinates):
                    valid_placements.append(coordinates)
        
        return valid_placements
