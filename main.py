"""
HANOI-NTM
Entry point for the Tower of Hanoi Nondeterministic Turing Machine simulator.
"""

from simulator import HanoiNTMSimulator


def main():
    """Create and run the simulator application."""
    app = HanoiNTMSimulator()
    app.run()


if __name__ == "__main__":
    main()
