import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple, Callable
from ..constants import BOARD_SIZE, WATER, SHIP, HIT, MISS, EMPTY
from ..game.board import Board

class BattleshipGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Battleship")
        self.cell_size = 40
        self.margin = 20
        
        # Create game boards
        board_width = BOARD_SIZE * self.cell_size + 2 * self.margin
        total_width = board_width * 2 + self.margin * 3
        window_height = BOARD_SIZE * self.cell_size + self.margin * 3
        
        self.root.geometry(f"{total_width}x{window_height}")
        
        # Player board canvas
        self.player_canvas = tk.Canvas(
            root, 
            width=board_width, 
            height=window_height
        )
        self.player_canvas.grid(row=0, column=0, padx=self.margin)
        
        # Computer board canvas
        self.computer_canvas = tk.Canvas(
            root, 
            width=board_width, 
            height=window_height
        )
        self.computer_canvas.grid(row=0, column=1, padx=self.margin)
        
        # Bind click event for computer's board
        self.computer_canvas.bind('<Button-1>', self.handle_click)
        
        # Store callback for shot processing
        self.process_shot_callback: Callable[[int, int], None] = None

    def draw_board(self, canvas: tk.Canvas, board: Board, hide_ships: bool = False):
        """Draw a game board on the specified canvas"""
        canvas.delete("all")
        
        # Draw grid
        for i in range(BOARD_SIZE + 1):
            # Vertical lines
            canvas.create_line(
                self.margin + i * self.cell_size, self.margin,
                self.margin + i * self.cell_size, self.margin + BOARD_SIZE * self.cell_size
            )
            # Horizontal lines
            canvas.create_line(
                self.margin, self.margin + i * self.cell_size,
                self.margin + BOARD_SIZE * self.cell_size, self.margin + i * self.cell_size
            )
            
            # Draw coordinates
            if i < BOARD_SIZE:
                # Row numbers
                canvas.create_text(
                    self.margin/2, 
                    self.margin + i * self.cell_size + self.cell_size/2,
                    text=str(i)
                )
                # Column numbers
                canvas.create_text(
                    self.margin + i * self.cell_size + self.cell_size/2,
                    self.margin/2,
                    text=str(i)
                )
        
        # Draw cells
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                cell = board.grid[y][x]
                
                # If hiding ships and it's a ship cell, show as empty unless hit
                if hide_ships and cell == SHIP:
                    cell = EMPTY
                
                color = self._get_cell_color(cell)
                if color:
                    canvas.create_rectangle(
                        self.margin + x * self.cell_size,
                        self.margin + y * self.cell_size,
                        self.margin + (x + 1) * self.cell_size,
                        self.margin + (y + 1) * self.cell_size,
                        fill=color
                    )
                
                # Show hits and misses
                if cell in [HIT, MISS]:
                    text = "X" if cell == HIT else "O"
                    canvas.create_text(
                        self.margin + x * self.cell_size + self.cell_size/2,
                        self.margin + y * self.cell_size + self.cell_size/2,
                        text=text,
                        fill="red" if cell == HIT else "blue"
                    )

    def _get_cell_color(self, cell: str) -> str:
        """Get the color for a cell based on its state"""
        colors = {
            WATER: "lightblue",
            SHIP: "gray",
            EMPTY: None,
            HIT: "pink",
            MISS: "lightcyan"
        }
        return colors.get(cell)

    def handle_click(self, event):
        """Handle click on the computer's board"""
        if not self.process_shot_callback:
            return
            
        # Convert click coordinates to grid position
        x = (event.x - self.margin) // self.cell_size
        y = (event.y - self.margin) // self.cell_size
        
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            self.process_shot_callback(x, y)

    def show_message(self, message: str):
        """Display a message box"""
        messagebox.showinfo("Battleship", message)

    def get_ship_placement(self, ship_name: str, length: int) -> List[Tuple[int, int]]:
        """Get ship placement from GUI input"""
        # TODO: Implement drag-and-drop ship placement
        # For now, we'll use a simple dialog
        placement_window = tk.Toplevel(self.root)
        placement_window.title(f"Place {ship_name}")
        placement_window.geometry("300x150")
        
        result = []
        
        def submit():
            nonlocal result
            try:
                x = int(start_x.get())
                y = int(start_y.get())
                if direction.get() == "h":
                    result = [(x + i, y) for i in range(length)]
                else:
                    result = [(x, y + i) for i in range(length)]
                placement_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid coordinates")
        
        tk.Label(placement_window, text=f"Place {ship_name} (length: {length})").pack()
        
        # Coordinate inputs
        coord_frame = tk.Frame(placement_window)
        coord_frame.pack(pady=5)
        tk.Label(coord_frame, text="X:").pack(side=tk.LEFT)
        start_x = tk.Entry(coord_frame, width=3)
        start_x.pack(side=tk.LEFT)
        tk.Label(coord_frame, text="Y:").pack(side=tk.LEFT)
        start_y = tk.Entry(coord_frame, width=3)
        start_y.pack(side=tk.LEFT)
        
        # Direction selection
        direction = tk.StringVar(value="h")
        tk.Radiobutton(placement_window, text="Horizontal", variable=direction, value="h").pack()
        tk.Radiobutton(placement_window, text="Vertical", variable=direction, value="v").pack()
        
        # Submit button
        tk.Button(placement_window, text="Place Ship", command=submit).pack(pady=10)
        
        # Wait for window to close
        placement_window.transient(self.root)
        placement_window.grab_set()
        self.root.wait_window(placement_window)
        
        return result

    def set_shot_callback(self, callback: Callable[[int, int], None]):
        """Set the callback for processing shots"""
        self.process_shot_callback = callback
