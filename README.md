# HANOI-NTM

A beginner-friendly desktop simulation of a **Nondeterministic Turing Machine (NTM)-style computation** using the Tower of Hanoi puzzle.

The project is written in Python and uses Tkinter for its graphical interface.

## Project overview

HANOI-NTM demonstrates how a machine can explore multiple possible computation paths. At each puzzle configuration, every legal move creates a separate computation branch. Each branch has its own puzzle configuration, two tapes, and move history.

A breadth-first search (BFS) scheduler explores branches in increasing path length. The scheduler is deterministic; the branching structure represents the machine's nondeterministic choices. BFS ensures that the first accepting branch is a shortest solution.

The machine accepts when at least one branch reaches the goal configuration, where all disks are on peg C.

## Features

- Tower of Hanoi puzzle with 1 to 5 disks.
- Three pegs: A, B, and C.
- Two independent tapes for every computation branch.
- Branch creation for each legal move.
- BFS-based branch exploration that finds a shortest solution.
- Global duplicate-configuration detection to avoid exploring the same puzzle state repeatedly.
- ACCEPT and REJECT branch statuses.
- Graphical display of the puzzle, tapes, computation branches, and results.
- Manual step-by-step and automatic execution controls.

## Project structure

```text
HANOI-NTM/
├── main.py
├── tape.py
├── hanoi.py
├── ntm.py
├── simulator.py
└── README.md
```

### File descriptions

| File | Responsibility |
|---|---|
| `main.py` | Entry point; launches the application. |
| `tape.py` | Implements a tape with read, write, move, load, and clone operations. |
| `hanoi.py` | Implements the Hanoi puzzle, legal moves, goal test, and configuration copying. |
| `ntm.py` | Creates independent computation branches and explores them using BFS. |
| `simulator.py` | Builds the Tkinter graphical interface and connects the other modules. |
| `README.md` | Project documentation and instructions. |

## Two-tape architecture

Each computation branch owns two independent tapes:

**Tape 1 — Configuration tape**

Stores the peg containing each disk. Its symbols are written in disk order, from disk 1 (smallest) to disk n (largest). For example, `1:A` means disk 1 is on peg A.

**Tape 2 — History tape**

Stores the sequence of moves taken along that branch. For example, `A->C` records a move from peg A to peg C.

When a branch creates children, each child receives its own puzzle copy and its own tapes. Changes in one branch therefore do not change another branch.

## How the simulation works

1. The user chooses the number of disks and presses **Reset**.
2. The initial configuration places every disk on peg A.
3. The machine finds all legal moves from the current configuration.
4. Each legal move creates a separate child computation branch.
5. The BFS scheduler explores pending branches using a queue.
6. A branch that reaches the goal is marked **ACCEPT**.
7. A configuration already discovered elsewhere is marked **PRUNED** and is not explored again. A branch with no legal moves is marked **REJECT**.
8. The machine accepts when one branch reaches the goal. If the search space is exhausted without an accepting branch, it rejects.

The global repeated-configuration check is valid here because a disk arrangement fully determines all legal future moves.

## Tower of Hanoi rules

- Only the top disk of a peg can be moved.
- Only one disk can be moved at a time.
- A larger disk cannot be placed on a smaller disk.
- The goal is to move all disks from peg A to peg C.

For n disks, the minimum number of moves in a standard Tower of Hanoi solution is:

`2^n - 1`

## NTM concepts demonstrated

- **Configuration:** The current arrangement of disks and the machine's stored tape information.
- **Transition:** A legal move from one configuration to another.
- **Nondeterministic branching:** Multiple legal next moves produce separate possible computation paths.
- **Computation branch:** One independent path through the computation tree.
- **Acceptance:** At least one branch reaches the goal state.
- **Rejection:** A branch cannot continue successfully.
- **BFS scheduler:** A queue-based method used by this simulator to explore shorter paths before longer ones, guaranteeing a minimum-move solution.

This is an educational NTM-style simulator for a finite puzzle. BFS is the simulator's exploration strategy; it is not itself nondeterminism.

## Requirements

- Python 3.10 or newer.
- Tkinter (included with many standard Python installations; on some Linux systems it may need to be installed separately).

No third-party Python packages are required.

## How to run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python3 main.py
```

4. Choose a disk count from 1 to 5.
5. Press **Reset**, then **Next Step** to explore one branch at a time, or press **Start** for automatic exploration.
6. Press **Stop** to pause automatic exploration.

## Controls

| Control | Action |
|---|---|
| Reset | Starts a new simulation with the selected disk count. |
| Next Step | Processes one pending computation branch. |
| Start | Begins automatic branch exploration. |
| Stop | Pauses automatic exploration. |

## Learning objective

This project connects Theory of Computation concepts to a familiar puzzle. It illustrates configurations, transitions, branching computation paths, tapes, and acceptance through a small interactive desktop application.
