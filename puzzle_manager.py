

import chess
import chess.pgn
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import json
import random
import argparse
from PIL import Image, ImageTk
import cairosvg, io
# --- TRANSLATIONS ---

TRANSLATIONS = {
    "en": {
"lang_name": "English",
"piece_set": "Piece Set","exit_window": "Close Window",
"board_size": "Board Size", "small": "Small", "medium": "Medium", "large": "Large","extra_large": "Extra Large", "huge": "Huge",
"orientation": "Orientation", "portrait": "Portrait", "landscape": "Landscape",
        "score": "Score", "done": "Done", "solved": "Solved", "attempts": "Attempts left",
        "hint": "Hint", "skip": "Skip (-5 pts)", "skip2":"Skip", "correct": "Correct", "solved_msg": "Solved!",
        "failed": "Failed", "out_of_attempts": "Out of attempts.", "white_turn": "WHITE TO MOVE",
        "black_turn": "BLACK TO MOVE", "no_puzzles": "No puzzles active",
        "load_pgn_msg": "Please load a PGN file via File -> Load",
        "file": "File", "view": "View", "history": "History", "progress": "Show Progress",
        "language": "Language", "dutch": "Nederlands", "english": "English", "reset": "Reset Progress...",
        "all_finished": "All puzzles finished!", "confirm_skip": "View solution? (-5 pts)",
        "reset_title": "Reset Progress", "reset_msg": "Are you sure you want to reset all progress for '{}'?",
        "perfect": "Perfect", "partial": "Solved", "failed_status": "Failed", "skipped": "Skipped",
        "review": "Review", "performance": "Performance Analysis", "total_puzzles": "Total Puzzles:",
        "avg_score": "Average Score:", "current_total": "Current Total:", "streak": "Longest Streak:",
        "exit": "Exit", "open_recent": "Open Recent", "load_pgn":"Load PGN...","progress_cleared":"Progress has been cleared.",
        "no_data_msg": "No data available yet.",
        "footer_msg": "Keep solving to reach your next milestone!", "chess_puzzle_manager":"Chess Puzzle Manager",
        "themes":"themes","puzzle_name":"Puzzle Name","status":"Status","settings": "Settings",
        "board_color": "Board Color", "color_green": "Classic Green", "color_blue": "Ocean Blue",
        "color_brown": "Wood Brown", "color_gray": "Modern Gray","back":"Back", "forward":"Forward", "close":"Close",
"color_purple": "Royal Purple",
"color_night": "Midnight Blue",
"color_sand": "Desert Sand",
"color_emerald": "Emerald Mint"
    },
    "nl": {
"lang_name": "Nederlands",
"piece_set": "Stukken-set","exit_window": "Venster sluiten","board_size": "Bordgrootte", "small": "Klein",
        "medium": "Gemiddeld", "large": "Groot","extra_large": "Extra Groot", "huge": "Gigantisch",
"orientation": "Oriëntatie", "portrait": "Staand", "landscape": "Liggend",
        "score": "Score", "done": "Klaar", "solved": "Opgelost", "attempts": "Pogingen over",
        "hint": "Hint", "skip": "Overslaan (-5 pnt)", "skip2":"Overslaan", "correct": "Correct", "solved_msg": "Opgelost!",
        "failed": "Fout", "out_of_attempts": "Geen pogingen meer over.", "white_turn": "WIT AAN ZET",
        "black_turn": "ZWART AAN ZET", "no_puzzles": "Geen puzzels actief",
        "load_pgn_msg": "Laad een PGN bestand via Bestand -> Laden",
        "file": "Bestand", "view": "Beeld", "history": "Geschiedenis", "progress": "Voortgang",
        "language": "Taal", "dutch": "Nederlands", "english": "English", "reset": "Voortgang wissen...",
        "all_finished": "Alle puzzels voltooid!", "confirm_skip": "Oplossing bekijken? (-5 pnt)",
        "reset_title": "Voortgang Wissen", "reset_msg": "Weet u zeker dat u de voortgang voor '{}' wilt wissen?",
        "perfect": "Perfect", "partial": "Opgelost", "failed_status": "Gefaald", "skipped": "Overgeslagen",
        "review": "Inspectie", "performance": "Prestatie Analyse", "total_puzzles": "Totaal Puzzels:",
        "avg_score": "Gem. Score:", "current_total": "Totaal Score:", "streak": "Langste Reeks:",
        "exit": "Afsluiten", "open_recent": "Recent geopend", "load_pgn":"Laad PGN...", "progress_cleared":"Voortgang verwijderd.",
        "no_data_msg": "Nog geen gegevens beschikbaar.",
        "footer_msg": "Blijf puzzelen om je volgende mijlpaal te bereiken!", "chess_puzzle_manager":"Schaak Puzzel Manager",
        "themes":"thema's","puzzle_name":"Puzzel Naam","status":"Status","settings": "Instellingen",
        "board_color": "Bordkleur", "color_green": "Klassiek Groen", "color_blue": "Oceaan Blauw",
        "color_brown": "Hout Bruin", "color_gray": "Modern Grijs",
"back": "Terug", "forward": "Verder", "close": "Sluiten",
"color_purple": "Koninklijk Paars",
"color_night": "Middernacht Blauw",
"color_sand": "Woestijnzand",
"color_emerald": "Smaragd Mint"
    },
    "de": {
"lang_name": "Deutsch","exit_window": "Fenster schließen","board_size": "Brettgröße",
        "small": "Klein",
        "medium": "Mittel",
        "large": "Groß",
        "extra_large": "Extragroß",
        "huge": "Riesig",
"orientation": "Ausrichtung", "portrait": "Hochformat", "landscape": "Querformat",
        "score": "Punktestand", "done": "Fertig", "solved": "Gelöst", "attempts": "Versuche übrig",
        "hint": "Hinweis", "skip": "Überspringen (-5 Pkt)", "skip2":"Überspringen", "correct": "Richtig", "solved_msg": "Gelöst!",
        "failed": "Falsch", "out_of_attempts": "Keine Versuche mehr.", "white_turn": "WEISS AM ZUG",
        "black_turn": "SCHWARZ AM ZUG", "no_puzzles": "Keine Rätsel aktiv",
        "load_pgn_msg": "Bitte laden Sie eine PGN-Datei über Datei -> Laden",
        "file": "Datei", "view": "Ansicht", "history": "Verlauf", "progress": "Fortschritt",
        "language": "Sprache", "dutch": "Nederlands", "english": "English", "reset": "Fortschritt zurücksetzen...",
        "all_finished": "Alle Rätsel abgeschlossen!", "confirm_skip": "Lösung anzeigen? (-5 Pkt)",
        "reset_title": "Fortschritt zurücksetzen", "reset_msg": "Sind Sie sicher, dass Sie den Fortschritt für '{}' löschen wollen?",
        "perfect": "Perfekt", "partial": "Gelöst", "failed_status": "Fehlgeschlagen", "skipped": "Übersprungen",
        "review": "Überprüfung", "performance": "Leistungsanalyse", "total_puzzles": "Rätsel insgesamt:",
        "avg_score": "Durchschn. Punkte:", "current_total": "Gesamtpunktzahl:", "streak": "Längste Serie:",
        "exit": "Beenden", "open_recent": "Zuletzt geöffnet", "load_pgn":"PGN laden...", "progress_cleared":"Fortschritt wurde gelöscht.",
        "no_data_msg": "Noch keine Daten verfügbar.",
        "footer_msg": "Löse weiter, um dein nächstes Ziel zu erreichen!", "chess_puzzle_manager":"Schach-Rätsel-Manager",
        "themes":"Themen","puzzle_name":"Rätselname","status":"Status","settings": "Einstellungen",
    "board_color": "Brettfarbe",
    "color_green": "Klassisches Grün",
    "color_blue": "Ozeanblau",
    "color_brown": "Holzbraun",
    "color_gray": "Modernes Grau",
"back": "Zurück", "forward": "Vorwärts", "close": "Schließen",
"color_purple": "Königliches Violett",
"color_night": "Mitternachtsblau",
"color_sand": "Wüstensand",
"color_emerald": "Smaragdgrün"
    },
    "fr": {
"lang_name": "Français","exit_window": "Fermer la fenêtre","board_size": "Taille du plateau",
        "small": "Petit",
        "medium": "Moyen",
        "large": "Grand",
        "extra_large": "Très grand",
        "huge": "Géant",
"orientation": "Orientation", "portrait": "Portrait", "landscape": "Paysage",
        "score": "Score", "done": "Terminé", "solved": "Résolu", "attempts": "Tentatives restantes",
        "hint": "Indice", "skip": "Passer (-5 pts)", "skip2":"Passer", "correct": "Correct", "solved_msg": "Résolu !",
        "failed": "Échec", "out_of_attempts": "Plus de tentatives.", "white_turn": "LES BLANCS JOUENT",
        "black_turn": "LES NOIRS JOUENT", "no_puzzles": "Aucun puzzle actif",
        "load_pgn_msg": "Veuillez charger un fichier PGN via Fichier -> Charger",
        "file": "Fichier", "view": "Affichage", "history": "Historique", "progress": "Progression",
        "language": "Langue", "dutch": "Nederlands", "english": "English", "reset": "Réinitialiser la progression...",
        "all_finished": "Tous les puzzles sont terminés !", "confirm_skip": "Voir la solution ? (-5 pts)",
        "reset_title": "Réinitialiser la progression", "reset_msg": "Voulez-vous vraiment réinitialiser la progression pour '{}' ?",
        "perfect": "Parfait", "partial": "Résolu", "failed_status": "Échoué", "skipped": "Passé",
        "review": "Examen", "performance": "Analyse de performance", "total_puzzles": "Total des puzzles :",
        "avg_score": "Score moyen :", "current_total": "Total actuel :", "streak": "Plus longue série :",
        "exit": "Quitter", "open_recent": "Ouvrir récents", "load_pgn":"Charger PGN...", "progress_cleared":"La progression a été effacée.",
        "no_data_msg": "Aucune donnée disponible pour le moment.",
        "footer_msg": "Continuez à résoudre pour atteindre votre prochain objectif !", "chess_puzzle_manager":"Gestionnaire de Puzzles d'Échecs",
        "themes":"thèmes","puzzle_name":"Nom du Puzzle","status":"Statut",
"settings": "Paramètres",
    "board_color": "Couleur du plateau",
    "color_green": "Vert classique",
    "color_blue": "Bleu océan",
    "color_brown": "Brun bois",
    "color_gray": "Gris moderne",
"back": "Précédent", "forward": "Suivant", "close": "Fermer",
"color_purple": "Pourpre Royal",
"color_night": "Bleu de Minuit",
"color_sand": "Sable du Désert",
"color_emerald": "Menthe Émeraude"
    },
    "es": {
"lang_name": "Español","exit_window": "Cerrar ventana","board_size": "Tamaño del tablero",
        "small": "Pequeño",
        "medium": "Mediano",
        "large": "Grande",
        "extra_large": "Muy grande",
        "huge": "Gigante",
"orientation": "Orientación", "portrait": "Retrato", "landscape": "Paisaje",
        "score": "Puntuación", "done": "Hecho", "solved": "Resuelto", "attempts": "Intentos restantes",
        "hint": "Pista", "skip": "Saltar (-5 pts)", "skip2":"Saltar", "correct": "Correcto", "solved_msg": "¡Resuelto!",
        "failed": "Fallo", "out_of_attempts": "Sin intentos restantes.", "white_turn": "JUEGAN BLANCAS",
        "black_turn": "JUEGAN NEGRAS", "no_puzzles": "No hay acertijos activos",
        "load_pgn_msg": "Cargue un archivo PGN a través de Archivo -> Cargar",
        "file": "Archivo", "view": "Ver", "history": "Historial", "progress": "Progreso",
        "language": "Idioma", "dutch": "Nederlands", "english": "English", "reset": "Reiniciar progreso...",
        "all_finished": "¡Todos los acertijos terminados!", "confirm_skip": "¿Ver solución? (-5 pts)",
        "reset_title": "Reiniciar progreso", "reset_msg": "¿Está seguro de que desea borrar el progreso de '{}'?",
        "perfect": "Perfecto", "partial": "Resuelto", "failed_status": "Fallido", "skipped": "Saltado",
        "review": "Revisión", "performance": "Análisis de rendimiento", "total_puzzles": "Total de acertijos:",
        "avg_score": "Puntuación media:", "current_total": "Total actual:", "streak": "Racha más larga:",
        "exit": "Salir", "open_recent": "Abrir recientes", "load_pgn":"Cargar PGN...", "progress_cleared":"Se ha borrado el progreso.",
        "no_data_msg": "Aún no hay datos disponibles.",
        "footer_msg": "¡Sigue resolviendo para alcanzar tu próximo hito!", "chess_puzzle_manager":"Gestor de Puzzles de Ajedrez",
        "themes":"temas","puzzle_name":"Nombre del Puzzle","status":"Estado",
"settings": "Ajustes",
    "board_color": "Color del tablero",
    "color_green": "Verde clásico",
    "color_blue": "Azul océano",
    "color_brown": "Marrón madera",
    "color_gray": "Gris moderno",
"back": "Atrás", "forward": "Adelante", "close": "Cerrar",
"color_purple": "Púrpura Real",
"color_night": "Azul Medianoche",
"color_sand": "Arena del Desierto",
"color_emerald": "Menta Esmeralda"
    }
}


def load_svg_piece(filename, size):
    """ Converts an SVG file to a Tkinter-compatible PhotoImage. """
    filepath = filename

    # English: Convert SVG to PNG in memory using cairosvg
    png_data = cairosvg.svg2png(url=filepath, output_width=size, output_height=size)

    # English: Open the PNG data with PIL and convert to Tkinter PhotoImage
    image = Image.open(io.BytesIO(png_data))
    return ImageTk.PhotoImage(image)


def load_images(piece_set, size=60):
    piece_images = {}
    # Use the selected piece_set)

    base_path = os.path.join("Images", piece_set)
    mapping = {'P': 'wP.svg', 'R': 'wR.svg', 'N': 'wN.svg', 'B': 'wB.svg', 'Q': 'wQ.svg', 'K': 'wK.svg',
               'p': 'bP.svg', 'r': 'bR.svg', 'n': 'bN.svg', 'b': 'bB.svg', 'q': 'bQ.svg', 'k': 'bK.svg'}
    for s, f in mapping.items():
        path = os.path.join(base_path, f)
        if os.path.exists(path):
            piece_images[s] = load_svg_piece(path, size)
    return piece_images


class Translator:
    def __init__(self, translations, default_lang="en"):
        self.translations = translations
        self.current_lang = default_lang
        # English: Use English as a fallback if a translation is missing
        self.fallback_lang = "en"

    def set_language(self, lang_code):
        """ Updates the current language selection. """
        if lang_code in self.translations:
            self.current_lang = lang_code

    def get_available_languages(self):
        """ Returns a list of tuples: (iso_code, readable_name) """
        # English: Extract the iso code (key) and the 'lang_name' value
        return [(code, lang_dict.get("lang_name", code))
                for code, lang_dict in self.translations.items()]

    def __call__(self, key):
        """
        The magic method that allows the object to be called like a function: t("key")
        """
        # English: Try to get the translation in the current language
        lang_dict = self.translations.get(self.current_lang, {})
        translation = lang_dict.get(key)

        if translation:
            return translation

        # English: Fallback logic if the key is missing in the current language
        return self.translations.get(self.fallback_lang, {}).get(key, key)

t = Translator(TRANSLATIONS, default_lang="en")

# --- ENGINE ---

class PuzzleEngine:
    def __init__(self, pgn_file):
        base_name = os.path.splitext(pgn_file)[0]
        self.save_file = f"{base_name}_results.json"

        # Load only the results log
        self._load_results()
        # Load puzzles from PGN

        self.puzzles = self._load_puzzles(pgn_file) if os.path.exists(pgn_file) else []

        # Calculate totals on the fly for the UI
        self.total_score = sum(r[1] for r in self.results_log)
        self.total_done = len(self.results_log)
        self.total_solved = len([r for r in self.results_log if r[1] > 0])

    def _load_results(self):
        """ Loads only the results_log from the JSON file. """
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    # Support both old format and new list format during transition
                    self.results_log = data.get("results_log", [])
                    self.current_index = data.get("current_index", -1)
            except:
                self.results_log = []
                self.current_index = 0
        return []

    def save_state(self):
        """ The only state we need to save is the log of results. """
        with open(self.save_file, 'w') as f:
            json.dump({
                "results_log": self.results_log,
                "current_index": self.current_index
            }, f)

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

    def get_resume_or_next_puzzle(self):
        """ Returns the last unfinished puzzle or a new random one. """
        played_indices = {r[0] for r in self.results_log}

        # Check if the current_index is already finished
        if self.current_index != -1 and self.current_index not in played_indices:
            return self.puzzles[self.current_index]

        # Exclude puzzles already present in the results_log
        played_indices = {r[0] for r in self.results_log}
        remaining = [i for i in range(len(self.puzzles)) if i not in played_indices]

        if not remaining: return None
        self.current_index = random.choice(remaining)
        return self.puzzles[self.current_index]


# --- CUSTOM WIDGETS ---

# --- HISTORY DETAIL WINDOW ---

class HistoryDetailWindow(tk.Toplevel):
    """ A window to review a completed puzzle with move highlighting and board markers. """

    def __init__(self, parent, puzzle,  score=None, t=None, board_theme=None, themes=None, piece_set=None, remarks = ""):
        super().__init__(parent)
        self.parent = parent
        self.piece_set = piece_set
        self.board_theme = board_theme
        self.themes = themes
        self.t = t
        self.title(f"{self.t('review')} {puzzle['event']}")

        # Create a container frame to hold both labels side by side
        header_frame = tk.Frame(self)
        header_frame.pack(pady=5)
        # Create the 'remarks' label on the left side

        if remarks:
            tk.Label(header_frame,
                 text=remarks,
                 font=("Arial", 14, "italic"),
                 fg=self.themes[self.board_theme]["alert"] ).pack(side=tk.LEFT, padx=(0, 5))

        # Header label with score
        score_text = f" ({self.t('score')}: {score})" if score is not None else ""
        tk.Label(header_frame, text=f"{self.t('review')} {puzzle['display_name']}{score_text}",
                 font=("Arial", 12, "bold")).pack( pady=5)
        self.puzzle = puzzle

        self.piece_images = {}
        self._load_images()

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

    def _load_images(self):
        """ Load pieces to fit 50x50 squares. """
        self.piece_images = load_images(self.piece_set, 50)

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

        ttk.Button(btn_frame, text="< "+self.t("back"), command=self._prev_move).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.t("forward")+" >", command=self._next_move).pack(side=tk.LEFT, padx=5)
        ttk.Button(self, text=self.t("close"), command=self.destroy).pack(pady=5)

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
        colors = self.themes[self.board_theme]
        for r in range(8):
            for c in range(8):
                f_idx = 7 - c if self.is_flipped else c
                r_idx = r if self.is_flipped else 7 - r
                sq = chess.square(f_idx, r_idx)
                # Use the theme colors
                base_color = colors["light"] if (r + c) % 2 == 0 else colors["dark"]

                outline = self.themes[self.board_theme]["initial_move"] if sq in self.last_move_squares else ""
                width = 3 if sq in self.last_move_squares else 1
                self.canvas.create_rectangle(c * size, r * size, (c + 1) * size, (r + 1) * size,
                                             fill=base_color, outline=outline, width=width)

        for square, piece in self.review_board.piece_map().items():
            f, r = chess.square_file(square), chess.square_rank(square)
            col, row = (7 - f, r) if self.is_flipped else (f, 7 - r)
            img = self.piece_images.get(piece.symbol())
            if img: self.canvas.create_image(col * size, row * size, image=img, anchor=tk.NW)


# --- HISTORY LIST WINDOW ---
class HistoryWindow(tk.Toplevel):
    def __init__(self, parent, engine, piece_set=None):
        super().__init__(parent)
        self.parent = parent
        self.piece_set = piece_set
        self.title(self.parent.t("history"))
        self.geometry("600x600")  # Slightly wider for larger fonts
        # Initialize the menu for this specific window
        self._setup_menu()

        self.results_log = engine.results_log
        self.puzzles = engine.puzzles

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
        columns = ("#", self.parent.t("puzzle_name"), self.parent.t("score"), self.parent.t("status"))
        self.tree = ttk.Treeview(self, columns=columns, show="headings",
                                 selectmode="browse", style="Touch.Treeview")

        for col in columns:
            self.tree.heading(col, text=col)
            # Adjust column widths for larger text
            width = 60 if col == "#" else 100 if col in [self.parent.t("score"), self.parent.t("status")] else 250
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

    def _setup_menu(self):
        """ Creates a menu bar for the History window. """
        # Create the main menu bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Add a "File" (Bestand) menu
        # We use the global translator 't' for the labels
        file_m = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=t("file"), menu=file_m)

        # Add the close option with a shortcut key (Alt+F4 is standard, but we add a command)
        file_m.add_command(
            label=t("exit_window"),
            command=self.destroy,
            accelerator="Ctrl+W"  # Visual hint for the user
        )

        # Optional - Bind Ctrl+W to close the window as well
        self.bind("<Control-w>", lambda e: self.destroy())

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
            HistoryDetailWindow(self, self.puzzles[int(val[0])], int(val[2]), t=self.parent.t,
                                board_theme=self.parent.board_theme, themes=self.parent.themes, piece_set=self.piece_set)


class ProgressWindow(tk.Toplevel):
    def __init__(self, parent, results_log):
        super().__init__(parent)
        self.parent = parent
        self.title(self.parent.t("progress"))
        # Reduced height from 550 to 500 to remove dead space
        self.geometry("600x500")

        # 1. Canvas for the chart
        # Increased height slightly to use more of the top area
        self.canvas = tk.Canvas(self, bg="#ffffff", width=500, height=260, relief="sunken", borderwidth=1)
        self.canvas.pack(pady=(20, 10), padx=40)

        if not results_log:
            self.canvas.create_text(250, 130, text=self.parent.t("no_data_msg"), fill="grey")
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
        stats_frame = tk.LabelFrame(self, text=f" {self.parent.t('performance')} ", padx=20, pady=15)
        stats_frame.pack(fill=tk.X, padx=40, pady=(10, 5))

        # Column configuration for even spacing
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(3, weight=1)

        tk.Label(stats_frame, text=self.parent.t("total_puzzles")).grid(row=0, column=0, sticky="w", pady=2)
        tk.Label(stats_frame, text=f"{total_puzzles}", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10,
                                                                                        sticky="w")

        tk.Label(stats_frame, text=f"{self.parent.t('avg_score')}:").grid(row=0, column=2, padx=(30, 0), sticky="w")
        tk.Label(stats_frame, text=f"{avg_score}", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=10,
                                                                                    sticky="w")

        tk.Label(stats_frame, text=f"{self.parent.t('current_total')}:").grid(row=1, column=0, sticky="w", pady=2)
        tk.Label(stats_frame, text=f"{current_score}", font=("Arial", 10, "bold"), fg="#2980b9").grid(row=1, column=1,
                                                                                                      padx=10,
                                                                                                      sticky="w")

        tk.Label(stats_frame, text=f"{self.parent.t('streak')}:").grid(row=1, column=2, padx=(30, 0), sticky="w")
        tk.Label(stats_frame, text=f"{max_streak} {self.parent.t('solved')}", font=("Arial", 10, "bold"), fg="#27ae60").grid(row=1,
                                                                                                          column=3,
                                                                                                          padx=10,
                                                                                                          sticky="w")

        # 4. Motivational Footer (Fills the remaining gap naturally)
        footer_note = tk.Label(self, text=self.parent.t("footer_msg"),
                               font=("Arial", 9, "italic"), fg="#7f8c8d")
        # anchor to bottom
        footer_note.pack(side=tk.BOTTOM, pady=15)

# --- MAIN APP ---

class ChessPuzzleApp(tk.Toplevel):
    def __init__(self, pgn_file=None):
        super().__init__()

        # 1. Load configuration first (to access recent files)
        self.config_data = self._load_config()
        self.field_size = self.config_data.get("field_size", 70)
        self.piece_set = self.config_data.get("piece_set", "staunty")
        self.lang = self.config_data.get("language", "en")
        # Load Board Theme from config
        # Default to green theme if not set
        self.board_theme = self.config_data.get("board_theme", "green")
        self.themes = {
            "green": {
                "light": "#ebecd0", "dark": "#779556", "frame": "#4e6138",
                "inner_line": "#3b4a2a", "initial_move": "#f5f682", "user_move": "#cedd6d",
                "alert": "#a93226"  # Deep brick red
            },
            "blue": {
                "light": "#dee3e6", "dark": "#8ca2ad", "frame": "#5a6a73",
                "inner_line": "#434f56", "initial_move": "#fff4d3", "user_move": "#bdc9cf",
                "alert": "#e67e22"  # Vibrant orange (stands out against blue)
            },
            "brown": {
                "light": "#f0d9b5", "dark": "#b58863", "frame": "#6d4c41",
                "inner_line": "#3e2723", "initial_move": "#cd9118", "user_move": "#ffcc33",
                "alert": "#b03a2e"  # Darker mahogany red
            },
            "gray": {
                "light": "#e0e0e0", "dark": "#a0a0a0", "frame": "#424242",
                "inner_line": "#212121", "initial_move": "#ffffff", "user_move": "#c0c0c0",
                "alert": "#444444"  # Strong charcoal (minimalist alert)
            },
            "purple": {
                "light": "#f1e3f1", "dark": "#9b719b", "frame": "#5e455e",
                "inner_line": "#3d2d3d", "initial_move": "#f6e495", "user_move": "#c9a9c9",
                "alert": "#8e44ad"
            },
            "night": {
                "light": "#4b5b6b", "dark": "#2c3e50", "frame": "#1a252f",
                "inner_line": "#0f161c", "initial_move": "#f1c40f", "user_move": "#5d6d7e",
                "alert": "#e74c3c"
            },
            "sand": {
                "light": "#f4f1ea", "dark": "#d2b48c", "frame": "#8b7355",
                "inner_line": "#5d4d39", "initial_move": "#cd9118", "user_move": "#e6ccac",
                "alert": "#a0522d"
            },
            "emerald": {
                "light": "#e0f2f1", "dark": "#4db6ac", "frame": "#00695c",
                "inner_line": "#004d40", "initial_move": "#fff176", "user_move": "#b2dfdb",
                "alert": "#00acc1"
            }
        }
        self.current_theme = self.themes[self.board_theme]
        self.t = lambda k: t(k)
        t.set_language(self.lang)
        self.title(self.t("chess_puzzle_manager"))
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

        self._load_images(self.field_size)
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
        self.menubar.add_cascade(label=self.t("file"), menu=file_menu)
        file_menu.add_command(label=self.t("load_pgn"), command=self._menu_load_pgn)

        recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label=self.t("open_recent"), menu=recent_menu)
        for path in self.config_data.get("recent_files", []):
            label = os.path.basename(path)
            recent_menu.add_command(label=label, command=lambda p=path: self._load_specific_pgn(p))

        file_menu.add_separator()
        file_menu.add_command(label=self.t("exit"), command=self._on_close)

        # --- NEW: Settings Menu ---
        settings_m = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.t("settings"), menu=settings_m)

        # Submenu: Language
        #self._setup_lang_menu(settings_m, self.t)

        lang_m = tk.Menu(settings_m, tearoff=0)
        settings_m.add_cascade(label=self.t("language"), menu=lang_m)
        for code, name in [("en", "English"), ("nl", "Nederlands"), ("de", "Deutsch"), ("fr", "Français"),
                           ("es", "Español")]:
            lang_m.add_command(label=name, command=lambda c=code: self._set_lang(c))

        # Submenu: Board Color
        color_m = tk.Menu(settings_m, tearoff=0)
        settings_m.add_cascade(label=self.t("board_color"), menu=color_m)
        color_m.add_command(label=self.t("color_green"), command=lambda: self._set_theme("green"))
        color_m.add_command(label=self.t("color_blue"), command=lambda: self._set_theme("blue"))
        color_m.add_command(label=self.t("color_brown"), command=lambda: self._set_theme("brown"))
        color_m.add_command(label=self.t("color_gray"), command=lambda: self._set_theme("gray"))
        # decorative themes
        color_m.add_separator()
        color_m.add_command(label=self.t("color_purple"), command=lambda: self._set_theme("purple"))
        color_m.add_command(label=self.t("color_night"), command=lambda: self._set_theme("night"))
        color_m.add_command(label=self.t("color_sand"), command=lambda: self._set_theme("sand"))
        color_m.add_command(label=self.t("color_emerald"), command=lambda: self._set_theme("emerald"))

        # English: Submenu for Piece Sets
        pieces_m = tk.Menu(settings_m, tearoff=0)
        settings_m.add_cascade(label=t("piece_set"), menu=pieces_m)

        # English: List available sets manually (or scan the Images folder)
        available_sets = ["tatiana", "staunty"]

        for p_set in available_sets:
            # English: capitalize() makes the menu look cleaner (e.g., 'Staunty')
            pieces_m.add_command(
                label=p_set.capitalize(),
                command=lambda s=p_set: self._set_piece_set(s)
            )

            # English: Submenu for Board Size
            size_m = tk.Menu(settings_m, tearoff=0)
            settings_m.add_cascade(label=t("board_size"), menu=size_m)

        # English: Mapping display keys to pixel values
        sizes = [
            ("small", 60),
            ("medium", 70),
            ("large", 77),
            ("extra_large", 84),
            ("huge", 90)
        ]

        for key, val in sizes:
            # English: We use l=val to capture the current size in the loop
            size_m.add_command(
                label=t(key),
                command=lambda v=val: self._set_field_size(v)
            )
        # English: Orientation Submenu
        orient_m = tk.Menu(settings_m, tearoff=0)
        settings_m.add_cascade(label=t("orientation"), menu=orient_m)
        orient_m.add_command(label=t("portrait"), command=lambda: self._set_orientation("portrait"))
        orient_m.add_command(label=t("landscape"), command=lambda: self._set_orientation("landscape"))

        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.t("view"), menu=view_menu)
        view_menu.add_command(label=self.t("history"), command=lambda: HistoryWindow(self, self.engine, piece_set=self.piece_set))
        view_menu.add_command(label=self.t("progress"), command=lambda: ProgressWindow(self, self.engine.results_log))

        view_menu.add_separator()
        view_menu.add_command(label=self.t("reset"), command=self._confirm_reset)

    def _setup_ui(self):
        self.header = tk.Frame(self, pady=10, bg="#f7f7f7")
        self.header.pack(fill=tk.X)
        self.lbl_overall = tk.Label(self.header, text="", font=("Segoe UI", 10), bg="#f7f7f7")
        self.lbl_overall.pack()
        self.lbl_event = tk.Label(self.header, text="", font=("Segoe UI", 12, "bold"), bg="#f7f7f7")
        self.lbl_event.pack()
        self.lbl_sub = tk.Label(self.header, text="", font=("Segoe UI", 9, "italic"), bg="#f7f7f7", fg="#555")
        self.lbl_sub.pack()
        self.lbl_turn = tk.Label(self.header, text="", font=("Segoe UI", 10, "bold"), bg="#f7f7f7", fg=self.themes[self.board_theme]["alert"])
        self.lbl_turn.pack()

        # English: 2. Board Container (The frame that holds both the board and the buttons)
        # Important: We don't pack it here, _arrange_layout will do that.
        self.board_container = tk.Frame(self)

        # 'relief=tk.RIDGE' creates a classic raised decorative edge
        self.outer_frame = tk.Frame(self.board_container,
                                    bg=self.current_theme["frame"],  # A warm wood-like brown
                                    bd=12,  # Thickness of the decorative frame
                                    relief=tk.RIDGE)  # Decorative 3D border style
        self.outer_frame.pack(pady=(20, 5), padx=5)

        # The 'inner_border' creates a thin dark inlay line between the frame and the board
        self.inner_border = tk.Frame(self.outer_frame, bg=self.current_theme["inner_line"], bd=2, relief=tk.FLAT)
        self.inner_border.pack()

        self.canvas = tk.Canvas(self.inner_border, width=self.field_size*8, height=self.field_size*8, bg="white", highlightthickness=0)
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self._on_click)
        self._arrange_layout()

        self.controls_under_board = tk.Frame(self.board_container, pady=10)
        self.controls_under_board.pack(fill=tk.X)
        self.lbl_attempts = tk.Label(self.controls_under_board, text="", font=("Segoe UI", 10, "bold"), fg=self.themes[self.board_theme]["alert"])
        self.lbl_attempts.pack(side=tk.LEFT, padx=(20, 10))

        self.btn_container = tk.Frame(self.controls_under_board)
        self.btn_container.pack(side=tk.RIGHT, padx=20)
        self.btn_hint = ttk.Button(self.btn_container, text="Hint", command=self._show_hint)
        self.btn_hint.pack(side=tk.LEFT, padx=5)
        self.btn_hint.pack_forget()

        self.skip_button = (ttk.Button(self.btn_container, text=self.t("skip"), command=self._skip))
        self.skip_button.pack(side=tk.LEFT, padx=5)

    def _set_orientation(self, mode):
        """ Updates orientation, saves to config and rearranges the UI. """
        self.config_data["orientation"] = mode
        self._save_config()
        self._arrange_layout()

    def _arrange_layout(self):
        """ Arranges the header and board based on portrait or landscape setting. """
        # English: First, 'forget' the current packing to reset the layout
        self.header.pack_forget()
        self.board_container.pack_forget()

        orientation = self.config_data.get("orientation", "portrait")

        if orientation == "portrait":
            # English: Header on top, board below
            self.header.pack(side=tk.TOP, fill=tk.X, pady=10)
            self.board_container.pack(side=tk.TOP, pady=(10, 5), padx=5)
        else:
            # English: Board on the left, header on the right
            self.board_container.pack(side=tk.LEFT, pady=20, padx=(20, 5))
            self.header.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
            # English: Optional - justify header text to the left in landscape
            self.lbl_overall.config(anchor="w")

    def _set_field_size(self, size):
        """ Updates the field size, reloads images at the new scale, and resizes the board. """
        self.field_size = size
        self.config_data["field_size"] = size
        self._save_config()

        # English: We must reload images because they need to be re-scaled to the new size
        self._load_images(size)

        # English: Update the canvas size and refresh everything
        canvas_width = size * 8
        self.canvas.config(width=canvas_width, height=canvas_width)
        self.refresh_board()

    def _setup_lang_menu(self, parent_menu, translator):
        """ Dynamically builds the language selection menu. """
        lang_menu = tk.Menu(parent_menu, tearoff=0)
        parent_menu.add_cascade(label=translator("language"), menu=lang_menu)

        # English: Loop through available languages from the translator object
        # for code, name in translator.get_available_languages():
        #     # English: We use 'l=code' in the lambda to capture the current value of code
        #     lang_menu.add_command(
        #         label=name,
        #         command=lambda l=code: self._set_lang(l)
        #     )
    def _set_lang(self, l):
        self.lang = l
        t.set_language(self.lang)
        self.config_data["language"] = l
        self._save_config()
        self._setup_menu()
        self.update_display()
        self.load_puzzle()

    def _set_piece_set(self, set_name):
        """ Updates the piece set, saves config, and reloads images. """
        self.config_data["piece_set"] = set_name
        self._save_config()

        # English: Reload the images with the new set
        self._load_images(self.field_size)

        # English: Refresh the board to show new pieces
        self.refresh_board()

    def _set_theme(self, theme_key):
        """ Updates the board theme and saves it to config. """
        self.board_theme = theme_key
        self.current_theme = self.themes[self.board_theme]
        self.config_data["board_theme"] = theme_key
        self._save_config()
        self.refresh_board()
        self.update_display()

    def update_display(self):
        if not self.engine: return
        self.lbl_overall.config(
            text=f"{self.t('score')}: {self.engine.total_score} | {self.t('done')}: {self.engine.total_done}")
        self.lbl_attempts.config(text=f"{self.t('attempts')}: {self.attempts_left}")
        if self.board: self.lbl_turn.config(text=self.t("white_turn") if self.board.turn else self.t("black_turn"),fg=self.themes[self.board_theme]["alert"])
        self.skip_button.config(text=self.t("skip"))
        self.lbl_attempts.config(fg=self.themes[self.board_theme]["alert"])
        self.lbl_turn.config(fg=self.themes[self.board_theme]["alert"])

    # --- BOARD RENDERING ---

    def refresh_board(self):
        if not self.canvas.winfo_exists(): return
        self.canvas.delete("all")
        size = self.field_size
        has_board = self.board is not None
        colors = self.themes[self.board_theme]  # Get current colors

        for r in range(8):
            for c in range(8):
                flipped = self.is_flipped if has_board else False
                f_idx, r_idx = (7 - c, r) if flipped else (c, 7 - r)
                sq = chess.square(f_idx, r_idx)
                # Pick color based on square parity
                color = colors["light"] if (r + c) % 2 == 0 else colors["dark"]
                outline, width = "", 1

                if has_board:
                    if sq == self.selected_square:
                        color = self.current_theme["user_move"]
                    elif sq == self.hint_square:
                        color = self.current_theme["user_move"]
                    if sq in self.last_move_squares: outline, width = self.current_theme["initial_move"], 4

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
        msg = self.t('reset_msg')
        msg = msg.replace("{}",filename)

        if messagebox.askyesno(self.t("reset_title"), msg):
            self.engine.reset_history()
            self.update_status_display()
            self.refresh_board()
            messagebox.showinfo(self.t("reset_title"), self.t("progress_cleared"))
            # Optional: reload the first puzzle to start fresh
            self.load_puzzle()

    # --- CORE LOGIC ---

    def load_puzzle(self):
        if not self.engine:
            return
        puzzle = self.engine.get_resume_or_next_puzzle()
        if not puzzle:
            messagebox.showinfo(self.t("done"), self.t("all_finished"))
            self.lbl_event.config(text=self.t("no_puzzles"))
            self.lbl_sub.config(text=self.t("load_pgn_msg"))
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
        if puzzle['themes']: sub_info.append(self.t('themes')+f": {puzzle['themes'].replace('_', ' ')}")
        if puzzle['date'] and puzzle['date'] not in ["", "????", "?.?.?", "????.??.??"]: sub_info.append(
            f"[{puzzle['date']}]")
        self.lbl_sub.config(text=" | ".join(sub_info))

        if puzzle['initial_move']:
            self.board.push(puzzle['initial_move'])
            self.last_move_squares = [puzzle['initial_move'].from_square, puzzle['initial_move'].to_square]
        else:
            self.last_move_squares = []

        self.is_flipped = (self.board.turn == chess.BLACK)
        self.lbl_turn.config(text=f"{self.t('white_turn') if self.board.turn else self.t('black_turn')}",
                             fg=self.themes[self.board_theme]["alert"])
        self.update_status_display()
        self.refresh_board()
        return True

    def _show_solution_and_continue(self, result_score=0, remarks=""):
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
        review = HistoryDetailWindow(self, p, result_score, t=self.t, board_theme=self.board_theme, themes=self.themes, piece_set=self.piece_set, remarks=remarks)
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
        size = self.field_size
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
        if self.solve_step >= len(p['solution']):
            puzzle_result = {3: 10, 2: 5, 1: 2}.get(self.attempts_left, 0)
            self.engine.total_score += puzzle_result
            self._show_solution_and_continue(puzzle_result, "Error in puzzle")
            return
        if move == p['solution'][self.solve_step]:
            self.btn_hint.pack_forget()
            self.hint_square = None
            self.board.push(move)
            self.last_move_squares = [move.from_square, move.to_square]
            self.solve_step += 1
            if self.solve_step >= len(p['solution']):
                puzzle_result = {3: 10, 2: 5, 1: 2}.get(self.attempts_left, 0)
                self.engine.total_score += puzzle_result
                #messagebox.showinfo(self.t("correct"), self.t("solved")+"!")
                self._show_solution_and_continue(puzzle_result,self.t("solved"))
            else:
                self.after(500, lambda: self._opp_move(p['solution'][self.solve_step]))
        else:
            self.attempts_left -= 1
            self.btn_hint.pack(side=tk.LEFT, padx=5)
            if self.attempts_left <= 0:
                #messagebox.showerror(self.t("failed"), self.t("out_of_attempts"))
                self._show_solution_and_continue(0, self.t("out_of_attempts"))
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
        if self.board and messagebox.askyesno(self.t("skip2"), self.t("confirm_skip")):
            self.engine.total_score -= 5
            self._show_solution_and_continue(-5, self.t("skip2"))

    def update_status_display(self):
        status_text = (f"{self.t('score')}: {self.engine.total_score} | "
                       f"{self.t('done')}: {self.engine.total_done} | "
                       f"{self.engine.total_done}: {self.engine.total_solved}")
        self.lbl_overall.config(text=status_text)
        self.lbl_attempts.config(text=f"{self.t('attempts')}: {self.attempts_left}")

    def _load_images(self, size=60):
        self.piece_images = load_images(self.piece_set, size)



    def _on_close(self):
        self.engine.save_state()
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
