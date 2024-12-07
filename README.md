# Battleship Game

This is a Python implementation of the classic Battleship game, featuring both graphical and console interfaces. Challenge an AI opponent that employs intelligent targeting strategies using a hunt/target strategy, where RNG is used to determine the initial target then the AI will target the same cell until it is hit or missed.

## Features

- Graphical User Interface (GUI) using tkinter
- Console-based interface option
- Smart AI opponent with hunt/target strategy
- Interactive ship placement
- Real-time game feedback

## Requirements

- Python 3.7 or higher
- tkinter (typically included with Python)
- pytest (for running tests)

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TRic769/Battleship_2
   cd Battleship_2
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

### GUI Mode (Default)

To start the game in GUI mode, run:
```bash
python -m src
```

### Console Mode
Edit `src/__main__.py` and set `use_gui=False` in the GameState initialization.