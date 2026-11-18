"""
tape.py
A simple tape with a movable read/write head.

Each computation branch will keep its own copies of the tapes.
"""


class Tape:
    def __init__(self, cells=None, blank="_"):
        """Create a tape from a list of cells."""
        self.blank = blank
        self.cells = list(cells) if cells else [blank]
        self.head = 0

    def read(self):
        """Return the symbol currently under the tape head."""
        return self.cells[self.head]

    def write(self, symbol):
        """Write a symbol in the current cell."""
        self.cells[self.head] = str(symbol)

    def move(self, direction):
        """
        Move the head one cell.
        direction can be 'L' (left), 'R' (right), or 'S' (stay).
        """
        if direction == "L":
            if self.head == 0:
                self.cells.insert(0, self.blank)
            else:
                self.head -= 1
        elif direction == "R":
            self.head += 1
            if self.head == len(self.cells):
                self.cells.append(self.blank)
        elif direction == "S":
            pass
        else:
            raise ValueError("Direction must be 'L', 'R', or 'S'.")

    def load(self, symbols):
        """Replace the tape contents and place the head at the first cell."""
        self.cells = list(symbols) if symbols else [self.blank]
        self.head = 0

    def clone(self):
        """Return an independent copy of this tape."""
        copied_tape = Tape(self.cells, self.blank)
        copied_tape.head = self.head
        return copied_tape

    def get_contents(self):
        """Return a copy of all tape cells."""
        return self.cells.copy()

    def __str__(self):
        """Display tape contents and mark the current head position."""
        marked_cells = self.cells.copy()
        marked_cells[self.head] = f"[{marked_cells[self.head]}]"
        return " ".join(marked_cells)
