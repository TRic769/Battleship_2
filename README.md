# Battleship Game

A command-line implementation of the classic Battleship game where you play against an AI opponent.

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd battleship
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

Run the game using:
```bash
python -m src
```

## How to Play

1. Place your ships by entering:
   - Start position (row,col format, e.g., "3,4")
   - Direction (h for horizontal, v for vertical)

2. During your turn:
   - Enter coordinates to fire (row,col format)
   - X marks a hit, O marks a miss
   - S shows your ships, ~ shows water

3. The game continues until all ships of one player are sunk.
