

import chess
import chess.pgn
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import json
import random
import argparse
from PIL import Image, ImageTk


# --- HISTORY DETAIL WINDOW ---

class HistoryDetailWindow(tk.Toplevel):
    """ A window to review a completed puzzle with move highlighting and board markers. """

    def __init__(self, parent, puzzle, original_images, score=None):
        super().__init__(parent)
        self.title(f"Review: {puzzle['event']}")
        # Header with score
        score_text = f" (Score: {score})" if score is not None else ""
        tk.Label(self, text=f"Review: {puzzle['display_name']}{score_text}",
                 font=("Arial", 12, "bold")).pack(pady=5)
        self.puzzle = puzzle

        self.review_images = {}
        self._scale_images(original_images)

        # Setup board logic: start from FEN
        self.review_board = chess.Board(puzzle['fen'])
        # Apply initial opponent mistake immediately
        if puzzle['initial_move']:
            self.review_board.push(puzzle['initial_move'])

        self.solution_moves = puzzle['solution']
        self.current_step = 0
        self.last_move_squares = []

        # Pre-generate SAN strings for the solution
        self.san_list = self._generate_all_san()
        # Set board orientation
        self.is_flipped = (self.review_board.turn == chess.BLACK)

        self._setup_ui()
        self._update_display()

    def _generate_all_san(self):
        """ Pre-generates SAN strings for the entire solution. """
        temp_board = chess.Board(self.puzzle['fen'])
        if self.puzzle['initial_move']:
            temp_board.push(self.puzzle['initial_move'])

        sans = []
        for m in self.solution_moves:
            sans.append(temp_board.san(m))
            temp_board.push(m)
        return sans

    def _scale_images(self, original_images):
        """ Resizes pieces to fit 50x50 squares. """
        mapping = {'P': 'wP.png', 'R': 'wR.png', 'N': 'wN.png', 'B': 'wB.png', 'Q': 'wQ.png', 'K': 'wK.png',
                   'p': 'bP.png', 'r': 'bR.png', 'n': 'bN.png', 'b': 'bB.png', 'q': 'bQ.png', 'k': 'bK.png'}
        for sym, path_name in mapping.items():
            path = os.path.join("Images", path_name)
            if os.path.exists(path):
                img = Image.open(path).resize((50, 50), Image.Resampling.LANCZOS)
                self.review_images[sym] = ImageTk.PhotoImage(img)

    def _setup_ui(self):
        self.canvas = tk.Canvas(self, width=400, height=400, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10, padx=10)

        # Move List using Text widget for formatting
        self.move_text = tk.Text(self, height=3, width=50, font=("Consolas", 10),
                                 bg="#f0f0f0", relief=tk.FLAT, state=tk.DISABLED)
        self.move_text.pack(pady=5, padx=10)
        self.move_text.tag_configure("active", font=("Consolas", 10, "bold"), foreground="#1565c0",
                                     background="#d1e3ff")

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="< Back", command=self._prev_move).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Forward >", command=self._next_move).pack(side=tk.LEFT, padx=5)
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=5)

    def _update_display(self):
        """ Sync board and text highlighting. """
        if self.current_step > 0:
            last_m = self.solution_moves[self.current_step - 1]
            self.last_move_squares = [last_m.from_square, last_m.to_square]
        else:
            self.last_move_squares = []

        self.refresh_board()

        self.move_text.config(state=tk.NORMAL)
        self.move_text.delete("1.0", tk.END)
        self.move_text.insert(tk.END, "Solution: ")

        for i, san in enumerate(self.san_list):
            start_idx = self.move_text.index(tk.INSERT)
            self.move_text.insert(tk.END, san)
            end_idx = self.move_text.index(tk.INSERT)
            if i == self.current_step - 1:
                self.move_text.tag_add("active", start_idx, end_idx)
            self.move_text.insert(tk.END, " ")
        self.move_text.config(state=tk.DISABLED)

    def _next_move(self):
        if self.current_step < len(self.solution_moves):
            self.review_board.push(self.solution_moves[self.current_step])
            self.current_step += 1
            self._update_display()

    def _prev_move(self):
        if self.current_step > 0:
            self.review_board.pop()
            self.current_step -= 1
            self._update_display()

    def refresh_board(self):
        self.canvas.delete("all")
        size = 400 // 8
        for r in range(8):
            for c in range(8):
                f_idx = 7 - c if self.is_flipped else c
                r_idx = r if self.is_flipped else 7 - r
                sq = chess.square(f_idx, r_idx)
                base_color = "#ebecd0" if (r + c) % 2 == 0 else "#779556"
                outline = "#1565c0" if sq in self.last_move_squares else ""
                width = 3 if sq in self.last_move_squares else 1
                self.canvas.create_rectangle(c * size, r * size, (c + 1) * size, (r + 1) * size,
                                             fill=base_color, outline=outline, width=width)

        for square, piece in self.review_board.piece_map().items():
            f, r = chess.square_file(square), chess.square_rank(square)
            col, row = (7 - f, r) if self.is_flipped else (f, 7 - r)
            img = self.review_images.get(piece.symbol())
            if img: self.canvas.create_image(col * size, row * size, image=img, anchor=tk.NW)


# --- HISTORY LIST WINDOW ---
class HistoryWindow(tk.Toplevel):
    def __init__(self, parent, engine, piece_images):
        super().__init__(parent)
        self.parent = parent
        self.title("Puzzle History")
        self.geometry("600x600")  # Slightly wider for larger fonts

        self.results_log = engine.results_log
        self.puzzles = engine.puzzles
        self.piece_images = piece_images

        # --- Touch Friendly Style Configuration ---
        self.style = ttk.Style()
        # Set row height to 45 and font size to 12 for the body
        self.style.configure("Touch.Treeview",
                             rowheight=45,
                             font=('Arial', 12))
        # Set font size for the headers as well
        self.style.configure("Touch.Treeview.Heading",
                             font=('Arial', 12, 'bold'))

        # 1. List section setup using the Touch style
        columns = ("#", "Puzzle Name", "Score", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings",
                                 selectmode="browse", style="Touch.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            # Adjust column widths for larger text
            width = 60 if col == "#" else 100 if col in ["Score", "Status"] else 250
            self.tree.column(col, width=width)

        # Result coloring (remains same)
        self.tree.tag_configure("perfect", foreground="#27ae60")
        self.tree.tag_configure("partial", foreground="#f39c12")
        self.tree.tag_configure("failed", foreground="#e74c3c")
        self.tree.tag_configure("skipped", foreground="#95a5a6")

        self.item_ids = []
        for idx, score in self.results_log:
            p = self.puzzles[idx]
            name = p.get('display_name') or p.get('event')
            status = "Perfect" if score == 10 else "Solved" if score > 0 else "Failed" if score == 0 else "Skipped"
            tag = "perfect" if score == 10 else "partial" if score > 0 else "failed" if score == 0 else "skipped"

            item_id = self.tree.insert("", tk.END, values=(idx, name, score, status), tags=(tag,))
            self.item_ids.append(item_id)

        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self._open_detail())

        # 2. Navigation Footer (Larger buttons for touch)
        footer = tk.Frame(self, pady=15)
        footer.pack(fill=tk.X)

        # Larger padding and wider buttons
        self.btn_prev = ttk.Button(footer, text=" << ", width=8, command=self._prev_item)
        self.btn_prev.pack(side=tk.LEFT, padx=20)

        max_idx = max(0, len(self.item_ids) - 1)
        self.nav_slider = ttk.Scale(footer, from_=0, to=max_idx, orient=tk.HORIZONTAL, command=self._on_slider_move)
        self.nav_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_next = ttk.Button(footer, text=" >> ", width=8, command=self._next_item)
        self.btn_next.pack(side=tk.RIGHT, padx=20)

        # Initial selection logic
        if self.item_ids:
            if hasattr(self.parent, 'last_history_index') and self.parent.last_history_index < len(self.item_ids):
                if hasattr(self.parent, 'history_count_at_last_view') and len(
                        self.item_ids) > self.parent.history_count_at_last_view:
                    start_idx = len(self.item_ids) - 1
                else:
                    start_idx = self.parent.last_history_index
            else:
                start_idx = len(self.item_ids) - 1

            self.nav_slider.set(start_idx)
            self._on_slider_move(start_idx)
            self.parent.history_count_at_last_view = len(self.item_ids)

    def _on_slider_move(self, value):
        if not self.item_ids: return
        idx = int(float(value))
        if 0 <= idx < len(self.item_ids):
            target_id = self.item_ids[idx]
            if self.tree.selection() != (target_id,):
                self.tree.selection_set(target_id)
                self.tree.see(target_id)
            self.parent.last_history_index = idx

    def _on_tree_select(self, event):
        selected = self.tree.selection()
        if selected and selected[0] in self.item_ids:
            idx = self.item_ids.index(selected[0])
            self.nav_slider.set(idx)
            self.parent.last_history_index = idx

    def _prev_item(self):
        curr = int(float(self.nav_slider.get()))
        if curr > 0:
            self.nav_slider.set(curr - 1)
            self._on_slider_move(curr - 1)

    def _next_item(self):
        curr = int(float(self.nav_slider.get()))
        if curr < len(self.item_ids) - 1:
            self.nav_slider.set(curr + 1)
            self._on_slider_move(curr + 1)

    def _open_detail(self):
        selected = self.tree.selection()
        if selected:
            val = self.tree.item(selected[0], "values")
            HistoryDetailWindow(self, self.puzzles[int(val[0])], self.piece_images, int(val[2]))


class ProgressWindow(tk.Toplevel):
    def __init__(self, parent, results_log):
        super().__init__(parent)
        self.title("Progress Tracker & Statistics")
        # Reduced height from 550 to 500 to remove dead space
        self.geometry("600x500")

        # 1. Canvas for the chart
        # Increased height slightly to use more of the top area
        self.canvas = tk.Canvas(self, bg="#ffffff", width=500, height=260, relief="sunken", borderwidth=1)
        self.canvas.pack(pady=(20, 10), padx=40)

        if not results_log:
            self.canvas.create_text(250, 130, text="No data available yet.", fill="grey")
            return

        # --- Data Calculation (Same as before) ---
        total_puzzles = len(results_log)
        current_score = sum(r[1] for r in results_log)

        max_streak = 0
        current_streak = 0
        for _, score in results_log:
            if score > 0:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        avg_score = round(current_score / total_puzzles, 2) if total_puzzles > 0 else 0
        cumulative_scores = []
        c_sum = 0
        for _, s in results_log:
            c_sum += s
            cumulative_scores.append(c_sum)

        # --- Chart Drawing Logic ---
        padding = 40
        w, h = 500 - (2 * padding), 260 - (2 * padding)
        max_s, min_s = max(cumulative_scores), min(cumulative_scores)
        val_range = max_s - min_s if max_s != min_s else 10

        # Axis and Grid
        self.canvas.create_line(padding, 260 - padding, 500 - padding, 260 - padding, width=2)
        self.canvas.create_line(padding, padding, padding, 260 - padding, width=2)

        for i in range(5):
            val = min_s + (i * val_range / 4)
            y = (260 - padding) - (i * h / 4)
            self.canvas.create_line(padding, y, 500 - padding, y, fill="#eeeeee")
            self.canvas.create_text(padding - 10, y, text=f"{int(val)}", anchor=tk.E, font=("Arial", 8))

        x_step = w / (total_puzzles - 1) if total_puzzles > 1 else w
        points = []
        for i, s in enumerate(cumulative_scores):
            x = padding + (i * x_step)
            y = (260 - padding) - ((s - min_s) / val_range * h)
            points.extend([x, y])
            dot_color = "#3498db" if i < total_puzzles - 1 else "#e74c3c"
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=dot_color, outline=dot_color)

        if len(points) >= 4:
            self.canvas.create_line(points, fill="#3498db", width=2, smooth=True)

        # --- Statistics Text Section ---
        # Use 'fill=tk.BOTH' and 'expand=False' to tighten the layout
        stats_frame = tk.LabelFrame(self, text=" Performance Analysis ", padx=20, pady=15)
        stats_frame.pack(fill=tk.X, padx=40, pady=(10, 5))

        # Column configuration for even spacing
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(3, weight=1)

        tk.Label(stats_frame, text="Total Puzzles:").grid(row=0, column=0, sticky="w", pady=2)
        tk.Label(stats_frame, text=f"{total_puzzles}", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10,
                                                                                        sticky="w")

        tk.Label(stats_frame, text="Average Score:").grid(row=0, column=2, padx=(30, 0), sticky="w")
        tk.Label(stats_frame, text=f"{avg_score}", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=10,
                                                                                    sticky="w")

        tk.Label(stats_frame, text="Current Total:").grid(row=1, column=0, sticky="w", pady=2)
        tk.Label(stats_frame, text=f"{current_score}", font=("Arial", 10, "bold"), fg="#2980b9").grid(row=1, column=1,
                                                                                                      padx=10,
                                                                                                      sticky="w")

        tk.Label(stats_frame, text="Longest Streak:").grid(row=1, column=2, padx=(30, 0), sticky="w")
        tk.Label(stats_frame, text=f"{max_streak} solved", font=("Arial", 10, "bold"), fg="#27ae60").grid(row=1,
                                                                                                          column=3,
                                                                                                          padx=10,
                                                                                                          sticky="w")

        # 4. Motivational Footer (Fills the remaining gap naturally)
        footer_note = tk.Label(self, text="Keep solving to reach your next milestone!",
                               font=("Arial", 9, "italic"), fg="#7f8c8d")
        # anchor to bottom
        footer_note.pack(side=tk.BOTTOM, pady=15)

class PuzzleEngine:
        def __init__(self, pgn_file):
            base_name = os.path.splitext(pgn_file)[0]
            self.save_file = f"{base_name}_results.json"

            # Load only the results log
            self.results_log = self._load_results()
            # Load puzzles from PGN

            self.puzzles = self._load_puzzles(pgn_file) if os.path.exists(pgn_file) else []

            # Calculate totals on the fly for the UI
            self.total_score = sum(r[1] for r in self.results_log)
            self.total_done = len(self.results_log)
            self.total_solved = len([r for r in self.results_log if r[1] > 0])

            self.current_index = -1

        def _load_results(self):
            """ Loads only the results_log from the JSON file. """
            if os.path.exists(self.save_file):
                try:
                    with open(self.save_file, 'r') as f:
                        data = json.load(f)
                        # Support both old format and new list format during transition
                        return data.get("results_log", [])
                except:
                    return []
            return []

        def save_state(self):
            """ The only state we need to save is the log of results. """
            with open(self.save_file, 'w') as f:
                json.dump({"results_log": self.results_log}, f)

        def reset_history(self):
            """ Clears all results and resets the save file. """
            self.results_log = []
            self.total_score = 0
            self.total_done = 0
            self.total_solved = 0
            self.save_state()  # Overwrites the file with empty log

        def _load_puzzles(self, filename):
            """ Reads PGN and extracts puzzle data including Lichess Site URL. """
            p_list = []
            try:
                with open(filename) as f:
                    while True:
                        game = chess.pgn.read_game(f)
                        if game is None: break
                        moves = list(game.mainline_moves())
                        w = game.headers.get("White", "").strip()
                        b = game.headers.get("Black", "").strip()

                        # Distinguish between training format (one mistake first) and normal PGN
                        is_training = "wins" in w.lower() or "wins" in b.lower()

                        if is_training:
                            initial_move = moves[0] if moves else None
                            solution = moves[1:] if moves else []
                            display_name = ""
                        else:
                            initial_move = None
                            solution = moves
                            names = [n for n in [w, b] if n and n != "?"]
                            display_name = " - ".join(names) if len(names) > 1 else (names[0] if names else "")

                        p_list.append({
                            'fen': game.headers.get("FEN"),
                            'initial_move': initial_move,
                            'solution': solution,
                            'display_name': display_name,
                            'date': game.headers.get("Date", ""),
                            'event': game.headers.get("Event", "Chess Puzzle"),
                            'site': game.headers.get("Site", ""),  # Link to Lichess
                            'rating': game.headers.get("Rating", "N/A"),
                            'themes': game.headers.get("Themes", "")
                        })
            except Exception as e:
                print(f"PGN Error: {e}")
            return p_list

        def get_next_random_puzzle(self):
            # Exclude puzzles already present in the results_log
            played_indices = {r[0] for r in self.results_log}
            remaining = [i for i in range(len(self.puzzles)) if i not in played_indices]

            if not remaining: return None
            self.current_index = random.choice(remaining)
            return self.puzzles[self.current_index]


# --- MAIN APP ---

class ChessPuzzleApp(tk.Toplevel):
    def __init__(self, pgn_file=None):
        super().__init__()
        self.title("Chess Puzzle Manager")

        # 1. Load configuration first (to access recent files)
        self.config_data = self._load_config()

        # 2. Determine which file to load
        target_file = None

        # Priority 1: Command line argument
        if pgn_file and os.path.exists(pgn_file):
            target_file = pgn_file
        # Priority 2: Check recent files list for the first valid file
        else:
            recent_list = self.config_data.get("recent_files", [])
            for path in recent_list:
                if os.path.exists(path):
                    target_file = path
                    break  # Found the most recent valid file

        # 3. Initialize Engine or Fallback
        if target_file:
            self.engine = PuzzleEngine(target_file)
            self._add_to_recent(target_file)
        else:
            self.engine = self._create_fallback_engine()

        self.board = None
        self.selected_square = None
        self.hint_square = None
        self.last_move_squares = []
        self.attempts_left = 3
        self.solve_step = 0
        self.is_flipped = False

        self._load_images()
        self._setup_menu()
        self._setup_ui()

        self.load_puzzle()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.resizable(False, False)
        self.last_history_index = 0
        self.history_count_at_last_view = 0

    # --- CONFIG & MENU ---

    def _load_config(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    return json.load(f)
            except:
                pass
        return {"recent_files": []}

    def _save_config(self):
        with open("config.json", "w") as f: json.dump(self.config_data, f)

    def _add_to_recent(self, filename):
        filename = os.path.abspath(filename)
        recent = self.config_data.get("recent_files", [])
        if filename in recent: recent.remove(filename)
        recent.insert(0, filename)
        self.config_data["recent_files"] = recent[:5]
        self._save_config()
        if hasattr(self, 'menubar'): self._setup_menu()

    def _setup_menu(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load PGN...", command=self._menu_load_pgn)

        recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Open Recent", menu=recent_menu)
        for path in self.config_data.get("recent_files", []):
            label = os.path.basename(path)
            recent_menu.add_command(label=label, command=lambda p=path: self._load_specific_pgn(p))

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)

        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="History", command=lambda: HistoryWindow(self, self.engine, self.piece_images))
        view_menu.add_command(label="Show Progress", command=lambda: ProgressWindow(self, self.engine.results_log))

        view_menu.add_separator()
        view_menu.add_command(label="Reset Progress...", command=self._confirm_reset)

    def _setup_ui(self):
        header = tk.Frame(self, pady=10, bg="#f7f7f7")
        header.pack(fill=tk.X)
        self.lbl_overall = tk.Label(header, text="", font=("Segoe UI", 10), bg="#f7f7f7")
        self.lbl_overall.pack()
        self.lbl_event = tk.Label(header, text="", font=("Segoe UI", 12, "bold"), bg="#f7f7f7")
        self.lbl_event.pack()
        self.lbl_sub = tk.Label(header, text="", font=("Segoe UI", 9, "italic"), bg="#f7f7f7", fg="#555")
        self.lbl_sub.pack()
        self.lbl_turn = tk.Label(header, text="", font=("Segoe UI", 10, "bold"), bg="#f7f7f7")
        self.lbl_turn.pack()

        self.canvas = tk.Canvas(self, width=480, height=480, bg="white", highlightthickness=0)
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self._on_click)

        footer = tk.Frame(self, pady=10)
        footer.pack(fill=tk.X)
        self.lbl_attempts = tk.Label(footer, text="", font=("Segoe UI", 10, "bold"), fg="#e74c3c")
        self.lbl_attempts.pack()

        self.btn_container = tk.Frame(footer)
        self.btn_container.pack()
        self.btn_hint = ttk.Button(self.btn_container, text="Hint", command=self._show_hint)
        self.btn_hint.pack(side=tk.LEFT, padx=5)
        self.btn_hint.pack_forget()

        ttk.Button(self.btn_container, text="Skip (-5 pts)", command=self._skip).pack(side=tk.LEFT, padx=5)

    # --- BOARD RENDERING ---

    def refresh_board(self):
        if not self.canvas.winfo_exists(): return
        self.canvas.delete("all")
        size = 480 // 8
        has_board = self.board is not None

        for r in range(8):
            for c in range(8):
                flipped = self.is_flipped if has_board else False
                f_idx, r_idx = (7 - c, r) if flipped else (c, 7 - r)
                sq = chess.square(f_idx, r_idx)
                color = "#ebecd0" if (r + c) % 2 == 0 else "#779556"
                outline, width = "", 1

                if has_board:
                    if sq == self.selected_square:
                        color = "#f6f669"
                    elif sq == self.hint_square:
                        color = "#82e0aa"
                    if sq in self.last_move_squares: outline, width = "#1565c0", 4

                self.canvas.create_rectangle(c * size, r * size, (c + 1) * size, (r + 1) * size, fill=color,
                                             outline=outline, width=width)

        if has_board:
            for sq, pc in self.board.piece_map().items():
                f, r = chess.square_file(sq), chess.square_rank(sq)
                col, row = (7 - f, r) if self.is_flipped else (f, 7 - r)
                img = self.piece_images.get(pc.symbol())
                if img: self.canvas.create_image(col * size, row * size, image=img, anchor=tk.NW)

    def _confirm_reset(self):
        """ Asks for confirmation and resets the engine state. """
        filename = os.path.basename(self.engine.save_file).replace("_results.json", ".pgn")
        msg = f"Are you sure you want to reset all progress for '{filename}'?"

        if messagebox.askyesno("Reset Progress", msg):
            self.engine.reset_history()
            self.update_status_display()
            self.refresh_board()
            messagebox.showinfo("Reset", "Progress has been cleared.")
            # Optional: reload the first puzzle to start fresh
            self.load_puzzle()

    # --- CORE LOGIC ---

    def load_puzzle(self):
        puzzle = self.engine.get_next_random_puzzle()
        if not puzzle:
            messagebox.showinfo("Done", "All puzzles finished!")
            self.lbl_event.config(text="No puzzles active")
            self.lbl_sub.config(text="Please load a PGN file via File -> Load")
            self.lbl_turn.config(text="")
            self.lbl_attempts.config(text="")
            self.btn_hint.pack_forget()

            self.board = None
            self.refresh_board()
            return False

        self.board = chess.Board(puzzle['fen'])
        self.solve_step = 0
        self.attempts_left = 3
        self.selected_square = self.hint_square = None

        # Header Cleanup
        main_title = (puzzle['display_name'] if puzzle['display_name'] else puzzle['event']).replace("? - ?", "")
        if puzzle['rating'] and puzzle['rating'] != "N/A": main_title += f" ({puzzle['rating']})"
        self.lbl_event.config(text=main_title)

        sub_info = []
        if puzzle['themes']: sub_info.append(f"Themes: {puzzle['themes'].replace('_', ' ')}")
        if puzzle['date'] and puzzle['date'] not in ["", "????", "?.?.?", "????.??.??"]: sub_info.append(
            f"[{puzzle['date']}]")
        self.lbl_sub.config(text=" | ".join(sub_info))

        if puzzle['initial_move']:
            self.board.push(puzzle['initial_move'])
            self.last_move_squares = [puzzle['initial_move'].from_square, puzzle['initial_move'].to_square]
        else:
            self.last_move_squares = []

        self.is_flipped = (self.board.turn == chess.BLACK)
        self.lbl_turn.config(text=f"{'WHITE' if self.board.turn else 'BLACK'} TO MOVE",
                             fg="#2980b9" if self.board.turn else "#2c3e50")
        self.update_status_display()
        self.refresh_board()
        return True

    def _show_solution_and_continue(self, result_score=0):
        """
        result_score should be an int:
        10 (perfect), 5/2 (partial), 0 (failed), -5 (skipped)
        """
        # If by any chance a string was passed, convert it to a default penalty
        if isinstance(result_score, str):
            result_score = -5 if result_score == "Skipped" else 0

        self.refresh_board()

        # Update the log with numerical data
        self.engine.results_log.append([self.engine.current_index, result_score])

        # Update live counters
        self.engine.total_score += result_score
        self.engine.total_done += 1
        if result_score > 0:
            self.engine.total_solved += 1

        self.engine.save_state()

        # Show the review window
        p = self.engine.puzzles[self.engine.current_index]
        review = HistoryDetailWindow(self, p, self.piece_images, result_score)
        self.wait_window(review)
        self.load_puzzle()

    def _create_fallback_engine(self):
        dummy = PuzzleEngine.__new__(PuzzleEngine)
        dummy.save_file = "temp_results.json"
        dummy.total_score = dummy.total_solved = dummy.total_done = 0
        dummy.played_history = {}
        dummy.results_log = []
        dummy.puzzles = [{
            'fen': 'r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4',
            'initial_move': None, 'solution': [chess.Move.from_uci("h5f7")],
            'display_name': "Example Puzzle", 'date': "2026", 'event': "No PGN Loaded",
            'site': "", 'rating': "Easy", 'themes': "mateIn1"
        }]
        return dummy

    def _load_specific_pgn(self, filename):
        if not os.path.exists(filename): return
        if self.engine: self.engine.save_state()
        self.engine = PuzzleEngine(filename)
        self._add_to_recent(filename)
        self.load_puzzle()

    def _menu_load_pgn(self):
        f = filedialog.askopenfilename(filetypes=(("PGN files", "*.pgn"), ("All files", "*.*")))
        if f: self._load_specific_pgn(f)

    def _on_click(self, event):
        if self.board is None: return
        size = 480 // 8
        c, r = event.x // size, event.y // size
        f, r_idx = (7 - c, r) if self.is_flipped else (c, 7 - r)
        sq = chess.square(f, r_idx)
        if self.selected_square is None:
            if self.board.piece_at(sq):
                self.selected_square = sq
                self.refresh_board()
        else:
            move = chess.Move(self.selected_square, sq)
            if self.board.piece_at(self.selected_square) and self.board.piece_at(
                    self.selected_square).piece_type == chess.PAWN:
                if (not self.is_flipped and r_idx == 7) or (
                        self.is_flipped and r_idx == 0): move.promotion = chess.QUEEN
            self._handle_move(move)
            self.selected_square = None
            self.refresh_board()

    def _handle_move(self, move):
        p = self.engine.puzzles[self.engine.current_index]
        if move == p['solution'][self.solve_step]:
            self.btn_hint.pack_forget()
            self.hint_square = None
            self.board.push(move)
            self.last_move_squares = [move.from_square, move.to_square]
            self.solve_step += 1
            if self.solve_step >= len(p['solution']):
                puzzle_result = {3: 10, 2: 5, 1: 2}.get(self.attempts_left, 0)
                self.engine.total_score += puzzle_result
                messagebox.showinfo("Correct", "Solved!")
                self._show_solution_and_continue(puzzle_result)
            else:
                self.after(500, lambda: self._opp_move(p['solution'][self.solve_step]))
        else:
            self.attempts_left -= 1
            self.btn_hint.pack(side=tk.LEFT, padx=5)
            if self.attempts_left <= 0:
                messagebox.showerror("Failed", "Out of attempts.")
                self._show_solution_and_continue(0)
            else:
                self.update_status_display()

    def _opp_move(self, move):
        self.board.push(move)
        self.last_move_squares = [move.from_square, move.to_square]
        self.solve_step += 1
        self.refresh_board()

    def _show_hint(self):
        self.hint_square = self.engine.puzzles[self.engine.current_index]['solution'][self.solve_step].from_square
        self.refresh_board()

    def _skip(self):
        if self.board and messagebox.askyesno("Skip", "View solution? (-5 pts)"):
            self.engine.total_score -= 5
            self._show_solution_and_continue(-5)

    def update_status_display(self):
        status_text = (f"Score: {self.engine.total_score} | "
                       f"Done: {self.engine.total_done} | "
                       f"Solved: {self.engine.total_solved}")
        self.lbl_overall.config(text=status_text)
        self.lbl_attempts.config(text=f"Attempts left: {self.attempts_left}")

    def _load_images(self):
        self.piece_images = {}
        mapping = {'P': 'wP.png', 'R': 'wR.png', 'N': 'wN.png', 'B': 'wB.png', 'Q': 'wQ.png', 'K': 'wK.png',
                   'p': 'bP.png', 'r': 'bR.png', 'n': 'bN.png', 'b': 'bB.png', 'q': 'bQ.png', 'k': 'bK.png'}
        for s, f in mapping.items():
            path = os.path.join("Images", f)
            if os.path.exists(path):
                img = Image.open(path).resize((60, 60), Image.Resampling.LANCZOS)
                self.piece_images[s] = ImageTk.PhotoImage(img)

    def _on_close(self):
        if self.engine: self.engine.save_state()
        self._save_config()
        self.master.destroy()


# --- [HistoryWindow & HistoryDetailWindow classes would follow here] ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default=None)  # Default is now None
    args = parser.parse_args()

    root = tk.Tk()
    root.withdraw()

    # Always start the app, even if args.filename is None
    app = ChessPuzzleApp(args.filename)
    root.mainloop()