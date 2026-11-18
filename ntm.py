"""
ntm.py
Creates independent computation branches and explores them using DFS.
"""

from dataclasses import dataclass, field

from hanoi import HanoiPuzzle
from tape import Tape


def configuration_key(puzzle):
    """Convert a puzzle configuration into a hashable value."""
    return tuple(tuple(puzzle.pegs[peg]) for peg in HanoiPuzzle.PEGS)


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
    visited: set = field(default_factory=set)


class NTMExplorer:
    """Explore Hanoi computation branches with a depth-first scheduler."""

    def __init__(self, disk_count):
        self.initial_puzzle = HanoiPuzzle(disk_count)
        self.branches = {}
        self.frontier = []
        self.next_branch_id = 0
        self.accepted_branch_id = None
        self.explored_count = 0
        self.rejected_count = 0
        self.finished = False

        root = self.initial_puzzle.clone()
        self._add_branch(
            parent_id=None,
            puzzle=root,
            history=[],
            move=None,
            visited={configuration_key(root)},
        )

    def _add_branch(self, parent_id, puzzle, history, move, visited,
                    status="PENDING", enqueue=True):
        """Create a branch with its own independent copies of both tapes."""
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
            status=status,
            visited=visited.copy(),
        )
        self.branches[branch_id] = branch

        if enqueue:
            self.frontier.append(branch_id)
        if status == "REJECT":
            self.rejected_count += 1

        return branch

    def step(self):
        """Expand one pending branch and return the branch that was processed."""
        if self.finished or not self.frontier:
            self.finished = True
            return None

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

        # Reverse insertion makes the first listed move explored first by DFS.
        for source, destination in reversed(legal_moves):
            child_puzzle = branch.puzzle.clone()
            child_puzzle.apply_move(source, destination)

            child_key = configuration_key(child_puzzle)
            child_history = branch.history + [f"{source}->{destination}"]
            child_visited = branch.visited | {child_key}

            # Reject a path that repeats one of its earlier configurations.
            # This prevents DFS from looping forever around Hanoi move cycles.
            if child_key in branch.visited:
                self._add_branch(
                    parent_id=branch_id,
                    puzzle=child_puzzle,
                    history=child_history,
                    move=(source, destination),
                    visited=child_visited,
                    status="REJECT",
                    enqueue=False,
                )
            else:
                self._add_branch(
                    parent_id=branch_id,
                    puzzle=child_puzzle,
                    history=child_history,
                    move=(source, destination),
                    visited=child_visited,
                )

        if not self.frontier:
            self.finished = True

        return branch

    def run_to_completion(self, max_steps=100000):
        """Run DFS until acceptance, exhaustion, or the safety limit."""
        steps = 0
        while not self.finished and steps < max_steps:
            self.step()
            steps += 1

        if steps >= max_steps and not self.finished:
            self.finished = True

        return self.get_result()

    def get_result(self):
        """Return the current solution and search statistics."""
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
        """Return branch data for the GUI's computation-tree display."""
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
        """Return a branch by its ID."""
        return self.branches.get(branch_id)
