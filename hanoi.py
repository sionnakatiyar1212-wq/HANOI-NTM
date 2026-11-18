"""
hanoi.py
Tower of Hanoi puzzle rules and configuration management.
"""


class HanoiPuzzle:
    PEGS = ("A", "B", "C")

    def __init__(self, disk_count):
        """Start with all disks stacked on peg A."""
        if not isinstance(disk_count, int) or disk_count < 1:
            raise ValueError("The number of disks must be a positive integer.")

        self.disk_count = disk_count
        # The largest disk is at index 0; the smallest is at the top.
        self.pegs = {
            "A": list(range(disk_count, 0, -1)),
            "B": [],
            "C": [],
        }

    def get_legal_moves(self):
        """Return every legal (source, destination) move."""
        moves = []

        for source in self.PEGS:
            if not self.pegs[source]:
                continue

            moving_disk = self.pegs[source][-1]

            for destination in self.PEGS:
                if source == destination:
                    continue

                if (
                    not self.pegs[destination]
                    or moving_disk < self.pegs[destination][-1]
                ):
                    moves.append((source, destination))

        return moves

    def apply_move(self, source, destination):
        """Apply one legal move. Return False if the move is illegal."""
        if (source, destination) not in self.get_legal_moves():
            return False

        disk = self.pegs[source].pop()
        self.pegs[destination].append(disk)
        return True

    def is_solved(self):
        """The puzzle is solved when every disk is on peg C."""
        return len(self.pegs["C"]) == self.disk_count

    def get_configuration(self):
        """Return a safe copy of the current peg arrangement."""
        return {peg: disks.copy() for peg, disks in self.pegs.items()}

    def get_tape_symbols(self):
        """
        Encode each disk's current peg as one tape symbol.
        The order is disk 1, disk 2, ..., disk n.
        """
        symbols = []

        for disk in range(1, self.disk_count + 1):
            for peg in self.PEGS:
                if disk in self.pegs[peg]:
                    symbols.append(f"{disk}:{peg}")
                    break

        return symbols

    def clone(self):
        """Create an independent puzzle copy for a computation branch."""
        copied_puzzle = HanoiPuzzle(self.disk_count)
        copied_puzzle.pegs = self.get_configuration()
        return copied_puzzle

    def __str__(self):
        """Return a readable representation of all three pegs."""
        return " | ".join(
            f"{peg}: {self.pegs[peg]}" for peg in self.PEGS
        )
