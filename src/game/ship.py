from dataclasses import dataclass
from typing import List, Tuple, Set

@dataclass
class Ship:
    name: str
    length: int
    coordinates: List[Tuple[int, int]]
    hits: Set[Tuple[int, int]] = None
    
    def __post_init__(self):
        """Initialize the hits set if not provided"""
        if self.hits is None:
            self.hits = set()
        
        # Validate that coordinates match the ship length
        if len(self.coordinates) != self.length:
            raise ValueError(f"Ship {self.name} requires exactly {self.length} coordinates")

    def hit(self, position: Tuple[int, int]) -> bool:
        """Register a hit on the ship"""
        if position in self.coordinates:
            self.hits.add(position)
            return True
        return False

    @property
    def is_sunk(self) -> bool:
        """Check if the ship is sunk"""
        return len(self.hits) == self.length
