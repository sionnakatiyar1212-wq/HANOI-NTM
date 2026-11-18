"""
ntm.py
A simple NTM-style computation tree explored using depth-first search.

Each branch owns an independent Hanoi configuration and two tape copies.
The DFS scheduler explores one branch at a time, while branching represents
the machine's nondeterministic choice among legal moves.
"""

from dataclasses import dataclass, field

from hanoi import HanoiPuzzle
from tape import Tape


@dataclass
class ComputationBranch:
    branch_id: int
    parent_id: int | None
    puzzle: HanoiPuzzle
    tape1: Tape
    tape2: Tape
    history: list = field(default_factory=list)
    move: tuple | None = None
    status: str = "PENDING"


class NTMExplorer:
    """Explore Tower of Hanoi computation branches with a DFS scheduler."""

    def __init__(self, disk_count):
        self.initial_puzzle = HanoiPuzzle(disk_count)
        self.branches = {}
        self.frontier = []
        self.next_branch_id = 0
        self.accepted_branch_id = None
        self.explored_count = 0
        self.rejected_count = 0
        self.finished = False
        self._add_branch(
            parent_id=None,
            puzzle=self.initial_puzzle.clone(),
            history=[],
            move=None,
        )

    def _add_branch(self, parent_id, puzzle, history, move):
        """Create a branch with its own two independent tapes."""
        branch_id = self.next_branch_id
        self.next_branch_id += 1

        tape1 = Tape(puzzle.get_tape_symbols())
        tape2 = Tape(history if history else ["START"])

        branch = ComputationBranch(
            branch_id=branch_id,
            parent_id=parent_id,
            puzzle=puzzle,
            tape1=tape1,
            tape2=tape2,
            history=history.copy(),
            move=move,
        )
        self.branches[branch_id] = branch
        self.frontier.append(branch_id)
        return branch

    def step(self):
        """
        Expand one pending branch.
        Returns the expanded branch, or None if no work remains.
        """
        if self.finished or not self.frontier:
            self.finished = True
            return None

        # Last-in, first-out order gives depth-first exploration.
        branch_id = self.frontier.pop()
        branch = self.branches[branch_id]
        self.explored_count += 1

        if branch.puzzle.is_solved():
            branch.status = "ACCEPT"
            self.accepted_branch_id = branch_id
            self.finished = True
            self.frontier.clear()
            return branch

        legal_moves = branch.puzzle.get_legal_moves()

        if not legal_moves:
            branch.status = "REJECT"
            self.rejected_count += 1
            if not self.frontier:
                self.finished = True
            return branch

        branch.status = "EXPANDED"

        # Add each legal next move as a separate computation branch.
        # Reversing preserves the puzzle's listed move order under a LIFO DFS.
        for source, destination in reversed(legal_moves):
            child_puzzle = branch.puzzle.clone()
            child_puzzle.apply_move(source, destination)

            move_text = f"{source}->{destination}"
            child_history = branch.history + [move_text]

            self._add_branch(
                parent_id=branch_id,
                puzzle=child_puzzle,
                history=child_history,
                move=(source, destination),
            )

        if not self.frontier:
            self.finished = True

        return branch

    def run_to_completion(self, max_steps=100000):
        """Run DFS until a branch accepts or the search is exhausted."""
        steps = 0
        while not self.finished and steps < max_steps:
            self.step()
            steps += 1

        if steps >= max_steps and not self.finished:
            self.finished = True

        return self.get_result()

    def get_result(self):
        """Return a summary of the current computation."""
        accepted = self.accepted_branch_id is not None
        solution = []

        if accepted:
            solution = self.branches[self.accepted_branch_id].history.copy()

        return {
            "accepted": accepted,
            "finished": self.finished,
            "solution": solution,
            "moves": len(solution),
            "explored_branches": self.explored_count,
            "rejected_branches": self.rejected_count,
            "pending_branches": len(self.frontier),
        }

    def get_branch_tree(self):
        """Return branch information suitable for displaying a tree."""
        return [
            {
                "branch_id": branch.branch_id,
                "parent_id": branch.parent_id,
                "move": branch.move,
                "status": branch.status,
                "history": branch.history.copy(),
                "configuration": branch.puzzle.get_configuration(),
            }
            for branch in self.branches.values()
        ]

    def get_branch(self, branch_id):
        """Return a branch by ID."""
        return self.branches.get(branch_id)
