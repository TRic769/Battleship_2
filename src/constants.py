# Board dimensions
BOARD_SIZE = 10  # Standard 10x10 grid

# Ship definitions
SHIPS = {
    'Carrier': 5,
    'Battleship': 4,
    'Cruiser': 3,
    'Submarine': 3,
    'Destroyer': 2
}

# Cell states
EMPTY = '.'      # Empty cell
SHIP = 'S'       # Cell containing a ship
MISS = 'O'       # Missed shot
HIT = 'X'        # Hit ship
WATER = '~'      # Water (for display purposes)
