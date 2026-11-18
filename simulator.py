"""
simulator.py
Tkinter graphical interface for the HANOI-NTM project.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ntm import NTMExplorer


class HanoiNTMSimulator:
    """Display the Hanoi puzzle, two tapes, and the NTM computation tree."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HANOI-NTM | Nondeterministic Turing Machine")
        self.root.geometry("1050x760")
        self.root.minsize(850, 650)

        self.explorer = None
        self.disk_count = tk.IntVar(value=3)
        self.current_branch = None
        self.auto_running = False

        self._build_interface()
        self.reset_simulation()

    def _build_interface(self):
        """Create all GUI sections."""
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="HANOI-NTM SIMULATOR",
            font=("Arial", 20, "bold"),
        ).pack(side="left")

        settings = ttk.Frame(self.root, padding=(12, 0, 12, 10))
        settings.pack(fill="x")

        ttk.Label(settings, text="Number of disks:").pack(side="left")
        self.disk_input = ttk.Spinbox(
            settings,
            from_=1,
            to=5,
            width=5,
            textvariable=self.disk_count,
        )
        self.disk_input.pack(side="left", padx=8)

        ttk.Button(settings, text="Reset", command=self.reset_simulation).pack(
            side="left", padx=5
        )
        ttk.Button(settings, text="Next Step", command=self.next_step).pack(
            side="left", padx=5
        )
        ttk.Button(settings, text="Start", command=self.start).pack(
            side="left", padx=5
        )
        ttk.Button(settings, text="Stop", command=self.stop).pack(
            side="left", padx=5
        )

        puzzle_frame = ttk.LabelFrame(
            self.root, text="Current Branch Configuration", padding=10
        )
        puzzle_frame.pack(fill="x", padx=12, pady=6)

        self.puzzle_canvas = tk.Canvas(
            puzzle_frame, height=210, background="white", highlightthickness=0
        )
        self.puzzle_canvas.pack(fill="x")

        tapes_frame = ttk.LabelFrame(self.root, text="Two Tapes", padding=10)
        tapes_frame.pack(fill="x", padx=12, pady=6)

        self.tape1_label = ttk.Label(tapes_frame, text="Tape 1: ")
        self.tape1_label.pack(anchor="w", pady=3)

        self.tape2_label = ttk.Label(tapes_frame, text="Tape 2: ")
        self.tape2_label.pack(anchor="w", pady=3)

        lower = ttk.Frame(self.root, padding=(12, 5))
        lower.pack(fill="both", expand=True)

        tree_frame = ttk.LabelFrame(
            lower, text="Computation Branches", padding=8
        )
        tree_frame.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.branch_tree = ttk.Treeview(
            tree_frame,
            columns=("parent", "move", "status"),
            show="headings",
            height=12,
        )
        self.branch_tree.heading("parent", text="Parent")
        self.branch_tree.heading("move", text="Move")
        self.branch_tree.heading("status", text="Status")
        self.branch_tree.column("parent", width=65, anchor="center")
        self.branch_tree.column("move", width=100, anchor="center")
        self.branch_tree.column("status", width=100, anchor="center")
        self.branch_tree.pack(fill="both", expand=True)

        result_frame = ttk.LabelFrame(lower, text="Machine Results", padding=8)
        result_frame.pack(side="right", fill="both", padx=(6, 0))

        self.status_label = ttk.Label(
            result_frame, text="Status: Ready", font=("Arial", 11, "bold")
        )
        self.status_label.pack(anchor="w", pady=5)

        self.stats_label = ttk.Label(
            result_frame, text="", justify="left", wraplength=220
        )
        self.stats_label.pack(anchor="w", pady=5)

        self.solution_label = ttk.Label(
            result_frame, text="Solution: Not found yet", wraplength=220
        )
        self.solution_label.pack(anchor="w", pady=5)

        footer = ttk.Label(
            self.root,
            text="Tape 1 = Current disk positions    |    Tape 2 = Move history",
            padding=8,
        )
        footer.pack(fill="x")

    def reset_simulation(self):
        """Create a fresh machine and clear the displayed results."""
        self.stop()

        try:
            count = self.disk_count.get()
            if count < 1 or count > 5:
                raise ValueError
        except (tk.TclError, ValueError):
            messagebox.showerror("Invalid input", "Choose between 1 and 5 disks.")
            return

        self.explorer = NTMExplorer(count)
        self.current_branch = self.explorer.get_branch(0)

        for item in self.branch_tree.get_children():
            self.branch_tree.delete(item)

        self.branch_tree.insert(
            "", "end", iid="0", values=("-", "START", "PENDING")
        )

        self._draw_puzzle(self.current_branch.puzzle)
        self._show_tapes(self.current_branch)
        self._update_results()
        self.status_label.config(text="Status: Ready")

    def _draw_puzzle(self, puzzle):
        """Draw the three pegs and disks on the canvas."""
        canvas = self.puzzle_canvas
        canvas.delete("all")

        width = max(canvas.winfo_width(), 700)
        base_y = 180
        peg_x = [width * 0.2, width * 0.5, width * 0.8]

        canvas.create_line(40, base_y, width - 40, base_y, width=3)

        for index, peg in enumerate(("A", "B", "C")):
            x = peg_x[index]
            canvas.create_line(x, 35, x, base_y, width=4, fill="#777777")
            canvas.create_text(x, 195, text=f"PEG {peg}", font=("Arial", 10, "bold"))

            disks = puzzle.pegs[peg]
            for level, disk in enumerate(disks):
                disk_width = 35 + disk * 22
                y_bottom = base_y - level * 22
                y_top = y_bottom - 18
                canvas.create_rectangle(
                    x - disk_width / 2,
                    y_top,
                    x + disk_width / 2,
                    y_bottom,
                    fill="#4b86c6",
                    outline="#24527a",
                    width=2,
                )
                canvas.create_text(x, (y_top + y_bottom) / 2, text=str(disk), fill="white")

    def _show_tapes(self, branch):
        """Display the contents of both tapes."""
        tape1 = " | ".join(branch.tape1.get_contents())
        tape2 = " | ".join(branch.tape2.get_contents())

        self.tape1_label.config(text=f"Tape 1 (configuration):  {tape1}")
        self.tape2_label.config(text=f"Tape 2 (history):  {tape2}")

    def _refresh_branch_tree(self):
        """Update existing rows and insert only newly created branches."""
        for info in self.explorer.get_branch_tree():
            branch_id = info["branch_id"]
            parent_id = info["parent_id"]
            move = info["move"]

            parent_text = "-" if parent_id is None else str(parent_id)
            move_text = "START" if move is None else f"{move[0]}->{move[1]}"
            values = (parent_text, move_text, info["status"])
            item_id = str(branch_id)

            if self.branch_tree.exists(item_id):
                self.branch_tree.item(item_id, values=values)
            else:
                self.branch_tree.insert(
                    "",
                    "end",
                    iid=item_id,
                    values=values,
                )

    def _update_results(self):
        """Update the machine status, statistics, and solution."""
        result = self.explorer.get_result()

        if result["accepted"]:
            self.status_label.config(text="Status: ACCEPT")
        elif result["finished"]:
            self.status_label.config(text="Status: REJECT")
        else:
            self.status_label.config(text="Status: RUNNING")

        total_created = len(self.explorer.branches)
        solution_line = (
            f"Solution length: {result['moves']} moves\n"
            if result["accepted"]
            else "Solution length: not found yet\n"
        )
        self.stats_label.config(
            text=(
                solution_line
                + f"Search effort (BFS steps): {result['explored_branches']}\n"
                f"Total branches created: {total_created}\n"
                f"Pruned duplicate branches: {result['pruned_branches']}\n"
                f"Dead-end (REJECT) branches: {result['rejected_branches']}\n"
                f"Pending branches: {result['pending_branches']}\n"
                f"Unique configurations seen: {result['unique_configurations']}"
            )
        )

        if result["accepted"]:
            solution = "  ".join(result["solution"])
            self.solution_label.config(
                text=f"Solution ({result['moves']} moves):\n{solution}"
            )
        else:
            self.solution_label.config(text="Solution: Not found yet")

    def next_step(self):
        """Explore exactly one pending computation branch."""
        if self.explorer is None or self.explorer.finished:
            return

        processed = self.explorer.step()
        if processed is not None:
            self.current_branch = processed
            self._draw_puzzle(processed.puzzle)
            self._show_tapes(processed)
            self._refresh_branch_tree()
            self._update_results()

    def start(self):
        """Begin automatic step-by-step exploration."""
        if self.explorer is None or self.explorer.finished:
            return
        if not self.auto_running:
            self.auto_running = True
            self._auto_step()

    def _auto_step(self):
        """Schedule the next automatic BFS step."""
        if not self.auto_running or self.explorer.finished:
            self.auto_running = False
            return

        self.next_step()
        if self.auto_running and not self.explorer.finished:
            self.root.after(100, self._auto_step)

    def stop(self):
        """Stop automatic exploration."""
        self.auto_running = False

    def run(self):
        """Start the Tkinter event loop."""
        self.root.mainloop()
