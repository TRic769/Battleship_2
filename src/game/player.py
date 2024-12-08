from typing import List, Tuple, Optional, Set
from random import randint
from enum import Enum
from .board import Board
from ..constants import BOARD_SIZE

class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

class AIPlayer:
    def __init__(self):
        self.shots: Set[Tuple[int, int]] = set()
        self.hits: List[Tuple[int, int]] = []
        self.hunt_mode = False
        self.last_hit: Optional[Tuple[int, int]] = None
        self.first_hit = 0
        self.current_direction: Optional[Direction] = None
        self.potential_directions: List[Direction] = []

    def get_shot(self, board: Board) -> Tuple[int, int]:
        """Get the next shot coordinates"""
        if not self.hunt_mode:
            return self._random_shot()
        return self._targeted_shot()

    def process_shot_result(self, x: int, y: int, hit: bool) -> None:
        """Process the result of the last shot"""
        self.shots.add((x, y))
        
        if hit:
            self.hits.append((x, y))
            self.hunt_mode = True
            self.last_hit = (x, y)
            
            if len(self.hits) == 1:  # First hit on a ship
                self.potential_directions = list(Direction)
                self.last_hit = self.first_hit    #Move the pointer to the first_hit
                if self.potential_directions:
                    self.potential_directions.pop()   #Skip one direction 

        else:
            if self.hunt_mode and self.current_direction:
                # Miss while hunting - try next direction
                self.current_direction = None

    def _random_shot(self) -> Tuple[int, int]:
        """Get a random valid shot position"""
        while True:
            x = randint(0, BOARD_SIZE - 1)
            y = randint(0, BOARD_SIZE - 1)
            if (x, y) not in self.shots:
                return x, y

    def _targeted_shot(self) -> Tuple[int, int]:
        """Get a targeted shot when hunting a ship"""
        if not self.last_hit:
            return self._random_shot()

        # If we don't have a direction, try a new one
        if not self.current_direction:
            while self.potential_directions:
                direction = self.potential_directions.pop()
                next_shot = self._get_next_position(self.last_hit, direction)
                if next_shot and next_shot not in self.shots:
                    self.current_direction = direction
                    return next_shot

            # If we've tried all directions around last hit,
            # try around a different hit point or go back to random
            self.hunt_mode = False
            return self._random_shot()

        # Continue in current direction
        next_shot = self._get_next_position(self.last_hit, self.current_direction)
        if next_shot and next_shot not in self.shots:
            return next_shot

        # If we can't continue in current direction, try opposite direction from first hit
        self.current_direction = None
        self.hits.clear() #The ship is sunk
        return self._targeted_shot()

    def _get_next_position(self, pos: Tuple[int, int], direction: Direction) -> Optional[Tuple[int, int]]:
        """Get the next position in the given direction"""
        x, y = pos
        dx, dy = direction.value
        new_x, new_y = x + dx, y + dy
        
        if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
            return new_x, new_y
        return None
