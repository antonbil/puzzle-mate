
import collections
import chess
import re
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
"analyze_db": "Analyze Database",
        "analysis_title": "Database Analysis",
        "db_overview": "Database Overview",
        "total_puzzles": "Total Puzzles",
        "rating_range": "Rating Range",
        "avg_rating": "Average Rating",
        "top_themes": "Top Themes",
        "no_puzzles_loaded": "No puzzles loaded to analyze.",
        "info": "Information",
        # Common Chess Themes
        "mate_in_1": "Mate in 1",
        "mate_in_2": "Mate in 2",
        "advantage": "Advantage",
        "endgame": "Endgame",
        "tactic": "Tactic",
"maintenance": "Maintenance",
        "run_validation": "Check for Invalid Puzzles",
        "validation_result": "Validation Result",
        "all_puzzles_valid": "All puzzles are structurally sound!",
        "errors_found": "Invalid puzzles detected",
        "score": "Score", "done": "Done", "solved": "Solved", "attempts": "Attempts left",
"menu_filter": "Filter Puzzles",
    "filter_title": "Search Filter",
    "filter_settings": "Filter Settings",
    "filter_theme": "Theme (contains):",
    "filter_rating_range": "Rating Range:",
    "apply_filter": "Apply",
    "puzzles_found": "puzzles found matching criteria.",
    "no_puzzles_found": "No puzzles found for these filters.",
    "min": "Min:",
    "max": "Max:",
    "clear": "Clear",
"enable_rating_filter": "Enable Rating Filter",
        "enable_theme_filter": "Enable Theme Filter",

    "filter_removed_msg": "Filter removed. Showing all puzzles.",
        "hint": "Hint", "skip": "Skip (-5 pts)", "skip2":"Skip", "correct": "Correct", "solved_msg": "Solved!",
        "failed": "Failed", "out_of_attempts": "Out of attempts.", "white_turn": "WHITE TO MOVE",
        "black_turn": "BLACK TO MOVE", "no_puzzles": "No puzzles active",
        "load_pgn_msg": "Please load a PGN file via File -> Load",
        "file": "File", "view": "View", "history": "History", "progress": "Show Progress",
        "language": "Language", "dutch": "Nederlands", "english": "English", "reset": "Reset Progress...",
        "all_finished": "All puzzles finished!", "confirm_skip": "View solution? (-5 pts)",
        "reset_title": "Reset Progress", "reset_msg": "Are you sure you want to reset all progress for '{}'?",
        "perfect": "Perfect", "partial": "Solved", "failed_status": "Failed", "skipped": "Skipped",
        "review": "Review", "performance": "Performance Analysis",
        "avg_score": "Average Score:", "current_total": "Current Total:", "streak": "Longest Streak:",
        "exit": "Exit", "open_recent": "Open Recent", "load_pgn":"Load PGN...","progress_cleared":"Progress has been cleared.",
        "no_data_msg": "No data available yet.",
        "footer_msg": "Keep solving to reach your next milestone!", "chess_puzzle_manager":"Chess Puzzle Manager",
        "themes":"themes","puzzle_name":"Puzzle Name","status":"Status","settings": "Settings",
        "board_color": "Board Color", "color_green": "Classic Green", "color_blue": "Ocean Blue",
        "color_brown": "Wood Brown", "color_gray": "Modern Gray","back":"Back", "forward":"Forward", "close":"Close",
"overall_progress_title": "Overall Progress Dashboard","overall_performance":"Overall Performance",'total_score':'Total Score',"file_url":"File url",
    "puzzles_solved": "puzzles solved in total",
"file_size": "File Size",
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
"analyze_db": "Analyseer Database",
        "analysis_title": "Database Analyse",
        "db_overview": "Database Overzicht",
        "total_puzzles": "Totaal aantal puzzels",
        "rating_range": "Rating bereik",
        "avg_rating": "Gemiddelde rating",
        "top_themes": "Belangrijkste thema's",
        "no_puzzles_loaded": "Geen puzzels geladen om te analyseren.",
        "info": "Informatie",
        # Veelvoorkomende Thema's
        "mate_in_1": "Mat in 1",
        "mate_in_2": "Mat in 2",
        "advantage": "Voordeel",
        "endgame": "Eindspel",
        "tactic": "Tactiek",
"maintenance": "Onderhoud",
"menu_filter": "Filter Puzzels",
    "filter_title": "Zoekfilter",
    "filter_settings": "Filter Instellingen",
    "filter_theme": "Thema (bevat):",
    "filter_rating_range": "Rating Bereik:",
    "apply_filter": "Toepassen",
    "puzzles_found": "puzzels gevonden die voldoen.",
    "no_puzzles_found": "Geen puzzels gevonden met deze filters.",
    "min": "Min:",
    "max": "Max:",
    "clear": "Wissen",
"remove_filter": "Filter Verwijderen",
"overall_progress_title": "Totaaloverzicht Voortgang","overall_performance":"Totale Voortgang",'total_score':'Totaal-Score',"file_url":"File url",
    "puzzles_solved": "puzzels in totaal opgelost","file_size": "Bestandsgrootte",
    "filter_removed_msg": "Filter verwijderd. Alle puzzels worden getoond.",
        "run_validation": "Check op ongeldige puzzels",
        "validation_result": "Validatie Resultaat",
        "all_puzzles_valid": "Alle puzzels zijn technisch in orde!",
        "errors_found": "Ongeldige puzzels gevonden",
        "score": "Score", "done": "Klaar", "solved": "Opgelost", "attempts": "Pogingen over",
        "hint": "Hint", "skip": "Overslaan (-5 pnt)", "skip2":"Overslaan", "correct": "Correct", "solved_msg": "Opgelost!",
        "failed": "Fout", "out_of_attempts": "Geen pogingen meer over.", "white_turn": "WIT AAN ZET",
        "black_turn": "ZWART AAN ZET", "no_puzzles": "Geen puzzels actief",
        "load_pgn_msg": "Laad een PGN bestand via Bestand -> Laden",
        "file": "Bestand", "view": "Tools", "history": "Geschiedenis", "progress": "Voortgang",
        "language": "Taal", "dutch": "Nederlands", "english": "English", "reset": "Voortgang wissen...",
        "all_finished": "Alle puzzels voltooid!", "confirm_skip": "Oplossing bekijken? (-5 pnt)",
        "reset_title": "Voortgang Wissen", "reset_msg": "Weet u zeker dat u de voortgang voor '{}' wilt wissen?",
        "perfect": "Perfect", "partial": "Opgelost", "failed_status": "Gefaald", "skipped": "Overgeslagen",
        "review": "Inspectie", "performance": "Prestatie Analyse",
        "avg_score": "Gem. Score:", "current_total": "Totaal Score:", "streak": "Langste Reeks:",
        "exit": "Afsluiten", "open_recent": "Recent geopend", "load_pgn":"Laad PGN...", "progress_cleared":"Voortgang verwijderd.",
        "no_data_msg": "Nog geen gegevens beschikbaar.",
        "footer_msg": "Blijf puzzelen om je volgende mijlpaal te bereiken!", "chess_puzzle_manager":"Schaak Puzzel Manager",
        "themes":"thema's","puzzle_name":"Puzzel Naam","status":"Status","settings": "Instellingen",
        "board_color": "Bordkleur", "color_green": "Klassiek Groen", "color_blue": "Oceaan Blauw",
        "color_brown": "Hout Bruin", "color_gray": "Modern Grijs",
"enable_rating_filter": "Rating-filter inschakelen",
        "enable_theme_filter": "Thema-filter inschakelen",
"back": "Terug", "forward": "Verder", "close": "Sluiten",
"color_purple": "Koninklijk Paars",
"color_night": "Middernacht Blauw",
"color_sand": "Woestijnzand",
"color_emerald": "Smaragd Mint"
    },
    "de": {
        "lang_name": "Deutsch",
        "piece_set": "Figurensatz",
        "exit_window": "Fenster schließen",
        "board_size": "Brettgröße",
        "small": "Klein",
        "medium": "Mittel",
        "large": "Groß",
        "extra_large": "Extra Groß",
        "huge": "Riesig",
        "orientation": "Ausrichtung",
        "portrait": "Hochformat",
        "landscape": "Querformat",
        "analyze_db": "Datenbank analysieren",
        "analysis_title": "Datenbank-Analyse",
        "db_overview": "Datenbank-Übersicht",
        "total_puzzles": "Gesamtanzahl Rätsel",
        "rating_range": "Rating-Bereich",
        "avg_rating": "Durchschnittliches Rating",
        "top_themes": "Top-Motive",
        "no_puzzles_loaded": "Keine Rätsel zum Analysieren geladen.",
        "info": "Information",
        # Common Chess Themes
        "mate_in_1": "Matt in 1",
        "mate_in_2": "Matt in 2",
        "advantage": "Vorteil",
        "endgame": "Endspiel",
        "tactic": "Taktik",
        "maintenance": "Wartung",
        "run_validation": "Auf ungültige Rätsel prüfen",
        "validation_result": "Validierungsergebnis",
        "all_puzzles_valid": "Alle Rätsel sind strukturell einwandfrei!",
        "errors_found": "Ungültige Rätsel gefunden",
        "score": "Punktzahl",
        "done": "Erledigt",
        "solved": "Gelöst",
        "attempts": "Verbleibende Versuche",
        "menu_filter": "Rätsel filtern",
        "filter_title": "Suchfilter",
        "filter_settings": "Filter-Einstellungen",
        "filter_theme": "Motiv (enthält):",
        "filter_rating_range": "Rating-Bereich:",
        "apply_filter": "Anwenden",
        "puzzles_found": "Rätsel gefunden, die den Kriterien entsprechen.",
        "no_puzzles_found": "Keine Rätsel für diese Filter gefunden.",
        "min": "Min:",
        "max": "Max:",
        "clear": "Löschen",
        "enable_rating_filter": "Rating-Filter aktivieren",
        "enable_theme_filter": "Motiv-Filter aktivieren",
        "filter_removed_msg": "Filter entfernt. Alle Rätsel werden angezeigt.",
        "hint": "Hinweis",
        "skip": "Überspringen (-5 Pkt)",
        "skip2": "Überspringen",
        "correct": "Richtig",
        "solved_msg": "Gelöst!",
        "failed": "Fehlgeschlagen",
        "out_of_attempts": "Keine Versuche mehr.",
        "white_turn": "WEISS IST AM ZUG",
        "black_turn": "SCHWARZ IST AM ZUG",
        "no_puzzles": "Keine aktiven Rätsel",
        "load_pgn_msg": "Bitte laden Sie eine PGN-Datei via Datei -> Laden",
        "file": "Datei",
        "view": "Ansicht",
        "history": "Verlauf",
        "progress": "Fortschritt anzeigen",
        "language": "Sprache",
        "dutch": "Nederlands",
        "english": "English",
        "reset": "Fortschritt zurücksetzen...",
        "all_finished": "Alle Rätsel abgeschlossen!",
        "confirm_skip": "Lösung anzeigen? (-5 Pkt)",
        "reset_title": "Fortschritt zurücksetzen",
        "reset_msg": "Sind Sie sicher, dass Sie den gesamten Fortschritt für '{}' zurücksetzen wollen?",
        "perfect": "Perfekt",
        "partial": "Gelöst",
        "failed_status": "Fehlgeschlagen",
        "skipped": "Übersprungen",
        "review": "Überprüfen",
        "performance": "Leistungsanalyse",
        "avg_score": "Durchschnittliche Punktzahl:",
        "current_total": "Aktueller Gesamtwert:",
        "streak": "Längste Serie:",
        "exit": "Beenden",
        "open_recent": "Zuletzt geöffnet",
        "load_pgn": "PGN laden...",
        "progress_cleared": "Der Fortschritt wurde gelöscht.",
        "no_data_msg": "Noch keine Daten verfügbar.",
        "footer_msg": "Löse weiter, um dein nächstes Ziel te erreichen!",
        "chess_puzzle_manager": "Schachrätsel-Manager",
        "themes": "Motive",
        "puzzle_name": "Rätselname",
        "status": "Status",
        "settings": "Einstellungen",
        "board_color": "Brettfarbe",
        "color_green": "Klassisches Grün",
        "color_blue": "Ozeanblau",
        "color_brown": "Holzbraun",
        "color_gray": "Modernes Grau",
        "back": "Zurück",
        "forward": "Vorwärts",
        "close": "Schließen",
        "overall_progress_title": "Gesamt-Fortschritt Dashboard",
        "overall_performance": "Gesamtleistung",
        "total_score": "Gesamtpunktzahl",
        "file_url": "Datei-URL",
        "puzzles_solved": "Rätsel insgesamt gelöst",
        "file_size": "Dateigröße",
        "color_purple": "Königliches Purpur",
        "color_night": "Mitternachtsblau",
        "color_sand": "Wüstensand",
        "color_emerald": "Smaragdminze"
    }
}


def load_svg_piece(filename, size):
    """ Converts an SVG file to a Tkinter-compatible PhotoImage. """
    filepath = filename

    # Convert SVG to PNG in memory using cairosvg
    png_data = cairosvg.svg2png(url=filepath, output_width=size, output_height=size)

    # Open the PNG data with PIL and convert to Tkinter PhotoImage
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
        # Use English as a fallback if a translation is missing
        self.fallback_lang = "en"

    def set_language(self, lang_code):
        """ Updates the current language selection. """
        if lang_code in self.translations:
            self.current_lang = lang_code

    def get_available_languages(self):
        """ Returns a list of tuples: (iso_code, readable_name) """
        # Extract the iso code (key) and the 'lang_name' value
        return [(code, lang_dict.get("lang_name", code))
                for code, lang_dict in self.translations.items()]

    def __call__(self, key):
        """
        The magic method that allows the object to be called like a function: t("key")
        """
        # Try to get the translation in the current language
        lang_dict = self.translations.get(self.current_lang, {})
        translation = lang_dict.get(key)

        if translation:
            return translation

        # Fallback logic if the key is missing in the current language
        return self.translations.get(self.fallback_lang, {}).get(key, key)

t = Translator(TRANSLATIONS, default_lang="en")


class MoveAnimator:
    def __init__(self, app):
        self.app = app
        self.canvas = app.canvas
        self.is_animating = False

    def animate(self, from_sq, to_sq, callback=None, reverse=False, steps=10, delay=15):
        self.is_animating = True

        # Find the piece. If reversing, it's currently at to_sq visually.
        search_sq = to_sq if reverse else from_sq
        piece_id = self.app.drawn_pieces.get(search_sq)

        if piece_id is None:
            self._finish(callback)
            return

        def get_pos(sq):
            f, r = chess.square_file(sq), chess.square_rank(sq)
            col, row = (7 - f, r) if self.app.is_flipped else (f, 7 - r)
            return col * self.app.field_size, row * self.app.field_size

        start_x, start_y = get_pos(from_sq)
        end_x, end_y = get_pos(to_sq)

        # --- CRUCIAL FIX ---
        # Manually place the piece at the start position on the canvas
        # BEFORE starting the animation loop, regardless of what the board state says.
        if reverse:
            self.canvas.coords(piece_id, end_x, end_y)
            target_x, target_y = start_x, start_y
        else:
            self.canvas.coords(piece_id, start_x, start_y)
            target_x, target_y = end_x, end_y

        self.canvas.tag_raise(piece_id)

        # Calculate movement per step
        curr_coords = self.canvas.coords(piece_id)
        dx = (target_x - curr_coords[0]) / steps
        dy = (target_y - curr_coords[1]) / steps

        def step(count):
            if count < steps:
                self.canvas.move(piece_id, dx, dy)
                self.app.after(delay, lambda: step(count + 1))
            else:
                self._finish(callback)

        step(0)

    def _finish(self, callback):
        self.is_animating = False
        if callback:
            callback()

class PuzzleValidator:
    """
    Utility class to verify the structural integrity of chess puzzles.
    Checks if FENs are valid and if all moves in the solution are legal.
    """

    def __init__(self, puzzles):
        # puzzles is the list of dictionaries from your _load_puzzles method
        self.puzzles = puzzles

    def validate_all(self):
        """
        Validates the entire list of puzzles.
        Returns a list of invalid puzzles with their reasons.
        """
        invalid_puzzles = []

        for index, p in enumerate(self.puzzles):
            reason = self._check_puzzle(p)
            if reason:
                invalid_puzzles.append({
                    'index': index + 1,
                    'name': p.get('display_name') or f"Puzzle #{index + 1}",
                    'reason': reason,
                    'site': p.get('site', '')
                })

        return invalid_puzzles

    def _check_puzzle(self, p):
        """
        Internal check for a single puzzle dictionary.
        Returns a string reason if invalid, None if valid.
        """
        try:
            # 1. Validate FEN
            board = chess.Board(p['fen'])
            if not board.is_valid():
                return "Invalid FEN/Starting Position"

            # 2. Check initial move (if present)
            if p['initial_move']:
                if p['initial_move'] not in board.legal_moves:
                    return f"Illegal initial move: {p['initial_move']}"
                board.push(p['initial_move'])

            # 3. Check solution sequence
            for i, move in enumerate(p['solution']):
                if move not in board.legal_moves:
                    # Return which move in the sequence failed
                    return f"Illegal move at step {i + 1}: {move}"
                board.push(move)

            return None  # Puzzle is valid
        except Exception as e:
            return f"System error during validation: {str(e)}"

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
        self.results_log = []
        self.current_index = 0
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    # Support both old format and new list format during transition
                    self.results_log = data.get("results_log", [])
                    self.current_index = data.get("current_index", -1)
            except:
                pass
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
                        'white': w,
                        'black': b,
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

    def analyze_database(self):
        """
        Analyzes the loaded puzzles (list of dicts) to extract statistical insights.
        All comments are in English as per instructions.
        """
        total = len(self.puzzles)
        themes_count = collections.Counter()
        ratings = []

        # Regex to find ratings inside parentheses like (2121) in player names
        rating_pattern = r"\((\d+)\)"

        for p in self.puzzles:
            # 1. Process Themes
            # If 'themes' is a string like "mateIn2, short", split by comma
            raw_themes = p.get('themes', '')
            if raw_themes:
                # Split by comma or semicolon and clean whitespace
                individual_themes = [t.strip() for t in re.split(r'[,;]', raw_themes) if t.strip()]
                for theme in individual_themes:
                    themes_count[theme] += 1
            else:
                # Fallback to 'event' if no themes are present
                event_theme = p.get('event', 'Unknown')
                themes_count[event_theme] += 1

            # 2. Extract Ratings
            # Check the 'rating' key first
            r_val = p.get('rating', 'N/A')

            # If rating is missing or N/A, try to extract from white/black names
            if r_val == "N/A" or not str(r_val).isdigit():
                full_names = p.get('white', '') + p.get('black', '')
                match = re.search(rating_pattern, full_names)
                if match:
                    r_val = match.group(1)

            try:
                # Only add to list if it's a valid integer
                if str(r_val).isdigit():
                    ratings.append(int(r_val))
            except ValueError:
                continue

        # Build the final statistics dictionary
        stats = {
            "total": total,
            "themes": dict(themes_count.most_common(30)),
            "min_rating": min(ratings) if ratings else "N/A",
            "max_rating": max(ratings) if ratings else "N/A",
            "avg_rating": sum(ratings) // len(ratings) if ratings else "N/A"
        }
        return stats

    def get_overall_progress_data(self, config_data):
        """
        Aggregates data using file size instead of puzzle counts for speed.
        """
        overall_files = []
        grand_total_solved = 0
        grand_total_score = 0
        # We can't really sum 'performance' easily with mixed file sizes,
        # so we'll focus on absolute totals.

        recent_files = config_data.get("recent_files", [])
        for file_path in recent_files:
            if not os.path.exists(file_path):
                continue

            base_path = os.path.splitext(file_path)[0]
            results_path = f"{base_path}_results.json"

            solved_count = 0
            file_score = 0

            if os.path.exists(results_path):
                try:
                    with open(results_path, 'r') as f:
                        data = json.load(f)
                        log = data.get("results_log", [])
                        solved_count = len(log)
                        file_score = sum(entry[1] for entry in log if len(entry) > 1)
                except Exception as e:
                    print(f"Error loading {results_path}: {e}")

            # Get file size in MB for a cleaner display
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = file_size_bytes / (1024 * 1024)

            overall_files.append({
                'name': os.path.basename(file_path),
                'full_path': file_path,
                'size_mb': file_size_mb,
                'solved': solved_count,
                'score': file_score
            })

            grand_total_solved += solved_count
            grand_total_score += file_score

        return {
            'files': overall_files,
            'total_score': grand_total_score,
            'total_solved': grand_total_solved
        }

    def get_overall_stats(self):
        """
        Gathers stats from config.json and the corresponding _results.json files.
        """
        overall_stats = []
        grand_total_puzzles = 0
        grand_total_solved = 0

        for file_path in self.recent_files:
            if not os.path.exists(file_path):
                continue

            # Matches your example: filename + "_results.json"
            base_path = os.path.splitext(file_path)[0]
            results_path = f"{base_path}_results.json"

            solved_count = 0
            total_score = 0

            if os.path.exists(results_path):
                try:
                    with open(results_path, 'r') as f:
                        data = json.load(f)
                        # solved_count is the number of entries in results_log
                        log = data.get("results_log", [])
                        solved_count = len(log)
                        # Sum of the second element in each pair [index, score]
                        total_score = sum(entry[1] for entry in log if len(entry) > 1)
                except Exception as e:
                    print(f"Error reading {results_path}: {e}")

            total_in_pgn = self._quick_count_pgn(file_path)

            overall_stats.append({
                'path': file_path,
                'name': os.path.basename(file_path),
                'total_count': total_in_pgn,
                'solved_count': solved_count,
                'score': total_score
            })

            grand_total_puzzles += total_in_pgn
            grand_total_solved += solved_count

        performance = (grand_total_solved / grand_total_puzzles * 100) if grand_total_puzzles > 0 else 0

        return {
            'files': overall_stats,
            'performance': performance,
            'total_score': sum(f['score'] for f in overall_stats)
        }


# --- CUSTOM WIDGETS ---
class FilterWindow(tk.Toplevel):
    def __init__(self, parent, stats):
        super().__init__(parent)
        self.parent = parent
        self.t = parent.t
        self.stats = stats

        self.title(self.t("filter_title"))
        # Increased height to show more themes at once
        self.geometry("480x800")
        self.configure(bg="#f8f9fa")
        self.resizable(False, False)

        # State variables
        self.use_theme = tk.BooleanVar(value=getattr(self.parent, 'last_use_theme', False))
        self.use_rating = tk.BooleanVar(value=getattr(self.parent, 'last_use_rating', False))
        self.selected_theme = tk.StringVar(value=getattr(self.parent, 'last_theme_filter', ""))

        # UI Header
        tk.Label(self, text=self.t("filter_settings"), font=("Segoe UI", 14, "bold"),
                 bg="#f8f9fa", fg="#2c3e50").pack(pady=10)

        # --- Rating Section ---
        rating_group = tk.LabelFrame(self, text=self.t("filter_rating_range"), bg="#f8f9fa", padx=10, pady=10)
        rating_group.pack(fill=tk.X, padx=30, pady=5)

        tk.Checkbutton(rating_group, text=self.t("enable_rating_filter"), variable=self.use_rating,
                       bg="#f8f9fa", command=self._toggle_entries).pack(anchor=tk.W)

        self.rating_frame = tk.Frame(rating_group, bg="#f8f9fa")
        self.rating_frame.pack(fill=tk.X, pady=5)

        tk.Label(self.rating_frame, text=self.t("min"), bg="#f8f9fa").pack(side=tk.LEFT)
        self.min_rating = ttk.Entry(self.rating_frame, width=8)
        self.min_rating.pack(side=tk.LEFT, padx=5)
        self.min_rating.insert(0, getattr(self.parent, 'last_min_rating', "0"))

        tk.Label(self.rating_frame, text=self.t("max"), bg="#f8f9fa").pack(side=tk.LEFT, padx=(10, 0))
        self.max_rating = ttk.Entry(self.rating_frame, width=8)
        self.max_rating.pack(side=tk.LEFT, padx=5)
        self.max_rating.insert(0, getattr(self.parent, 'last_max_rating', "3000"))

        # --- Theme Section ---
        theme_group = tk.LabelFrame(self, text=self.t("filter_theme"), bg="#f8f9fa", padx=10, pady=10)
        theme_group.pack(fill=tk.BOTH, expand=True, padx=30, pady=5)

        tk.Checkbutton(theme_group, text=self.t("enable_theme_filter"), variable=self.use_theme,
                       bg="#f8f9fa", command=self._toggle_entries).pack(anchor=tk.W)

        self.lbl_active_theme = tk.Label(theme_group, textvariable=self.selected_theme,
                                         fg="#2980b9", font=("Segoe UI", 10, "bold"), bg="#f8f9fa")
        self.lbl_active_theme.pack(pady=2)

        # --- Theme List Container ---
        self.theme_container = tk.Frame(theme_group, bg="white", relief=tk.SOLID, borderwidth=1)
        self.theme_container.pack(fill=tk.BOTH, expand=True, pady=5)

        # Create a dedicated style for the thick scrollbar
        style = ttk.Style()
        style.configure("Thick.Vertical.TScrollbar", width=25)  # Extra wide for Chromebook touch

        # Canvas with scrollbar visibility fix
        self.canvas = tk.Canvas(self.theme_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.theme_container, orient="vertical",
                                  command=self.canvas.yview, style="Thick.Vertical.TScrollbar")

        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        # Ensure the internal frame takes up the full width of the canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def _on_canvas_configure(event):
            # Update the width of the inner frame to match the canvas
            self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.canvas.bind("<Configure>", _on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the scrollbar FIRST to ensure visibility
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Populate themes
        for theme, count in stats['themes'].items():
            row = tk.Frame(self.scrollable_frame, bg="white", cursor="hand2")
            row.pack(fill=tk.X, pady=1, padx=2)  # Reduced pady to show more items

            display_name = self.t(theme.lower().replace(" ", "_")) or theme
            tk.Label(row, text=display_name, bg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=10)

            # Pushed count label to the far right with anchor and padx
            tk.Label(row, text=str(count), bg="white", fg="#95a5a6",
                     font=("Segoe UI", 9, "bold")).pack(side=tk.RIGHT, padx=15)

            for w in (row, row.winfo_children()[0], row.winfo_children()[1]):
                w.bind("<Button-1>", lambda e, t=theme: self._select_theme(t))
                # Hover effect
                w.bind("<Enter>", lambda e, r=row: r.configure(bg="#f0f7ff"))
                w.bind("<Leave>", lambda e, r=row: r.configure(bg="white"))

        # Mousewheel support for scrolling
        def _on_mousewheel(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all("<Button-4>", _on_mousewheel)
        self.canvas.bind_all("<Button-5>", _on_mousewheel)

        self._toggle_entries()

        # --- Action Buttons ---
        btn_frame = tk.Frame(self, bg="#f8f9fa")
        btn_frame.pack(fill=tk.X, padx=30, pady=15)

        ttk.Button(btn_frame, text=self.t("apply_filter"), command=self._apply).pack(side=tk.LEFT, expand=True,
                                                                                     fill=tk.X, padx=2)
        ttk.Button(btn_frame, text=self.t("remove_filter"), command=self._reset_filter).pack(side=tk.LEFT, expand=True,
                                                                                             fill=tk.X, padx=2)
        ttk.Button(btn_frame, text=self.t("cancel"), command=self.destroy).pack(side=tk.LEFT, expand=True, fill=tk.X,
                                                                                padx=2)

    def _select_theme(self, theme):
        """ Sets active theme and auto-enables the checkbox. """
        self.selected_theme.set(theme)
        self.use_theme.set(True)
        self._toggle_entries()

    def _toggle_entries(self):
        """ Enables/disables widgets based on checkboxes. """
        r_state = "normal" if self.use_rating.get() else "disabled"
        self.min_rating.config(state=r_state)
        self.max_rating.config(state=r_state)

        # Visual fade effect for the theme list
        alpha_bg = "white" if self.use_theme.get() else "#f0f0f0"
        self.scrollable_frame.config(bg=alpha_bg)
        self.canvas.config(bg=alpha_bg)

    def _apply(self):
        """ Applies logic and saves state to parent. """
        try:
            filters = {
                'use_theme': self.use_theme.get(),
                'use_rating': self.use_rating.get(),
                'theme': self.selected_theme.get(),
                'min_rating': int(self.min_rating.get() or 0),
                'max_rating': int(self.max_rating.get() or 9999)
            }
            # Persistence
            self.parent.last_use_theme = filters['use_theme']
            self.parent.last_use_rating = filters['use_rating']
            self.parent.last_theme_filter = filters['theme']
            self.parent.last_min_rating = str(filters['min_rating'])
            self.parent.last_max_rating = str(filters['max_rating'])

            self.parent.apply_advanced_filter(filters)
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for rating.")

    def _reset_filter(self):
        """ Removes all filters. """
        self.parent.last_use_theme = False
        self.parent.last_use_rating = False
        self.parent.reset_database_filter()
        self.destroy()

# --- HISTORY DETAIL WINDOW ---

class HistoryDetailWindow(tk.Toplevel):
    """ A window to review a completed puzzle with move highlighting and board markers. """

    def __init__(self, parent, puzzle,  score=None, t=None, board_theme=None, themes=None, piece_set=None, remarks = "", config=None):
        super().__init__(parent)
        self.drawn_pieces = {}
        self.parent = parent
        self.is_animating = False
        self.config_data = config
        self.field_size = self.config_data.get("field_size", 70)  * 5 // 6
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
        fen_ = puzzle['fen']
        self.review_board = chess.Board(fen_)
        self.initial_fen = fen_
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
        # Initialize the animator and link it to this window
        self.animator = MoveAnimator(self)
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
        self.piece_images = load_images(self.piece_set, self.field_size)

    def _setup_ui(self):
        # 1. Add a Menu Bar
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # File menu with Close option
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=self.t("file") or "File", menu=file_menu)
        file_menu.add_command(label=self.t("close"), command=self.destroy)

        # 2. Board Canvas
        self.canvas = tk.Canvas(
            self,
            width=8 * self.field_size,
            height=8 * self.field_size,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(pady=10, padx=10)

        # 3. Enhanced Move List Container (with Word Wrap)
        # We use a Text widget but make it look like a Frame
        self.move_text_container = tk.Text(
            self,
            height=4,
            bg="#f0f0f0",
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD,
            state=tk.DISABLED,
            cursor="arrow"
        )
        self.move_text_container.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # 4. Navigation Buttons (Close is now in the menu)
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="< " + self.t("back"), command=self._prev_move).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.t("forward") + " >", command=self._next_move).pack(side=tk.LEFT, padx=5)

    def _update_display(self):
        """ Renders moves as clickable objects using board logic for turn detection. """
        # Update board markers
        if self.current_step > 0:
            last_m = self.solution_moves[self.current_step - 1]
            self.last_move_squares = [last_m.from_square, last_m.to_square]
        else:
            self.last_move_squares = []
        self.refresh_board()

        # Clear and prepare the text container
        self.move_text_container.config(state=tk.NORMAL)
        self.move_text_container.delete("1.0", tk.END)

        # Use a temporary board to track the turn and move number
        temp_board = chess.Board(self.initial_fen)
        is_flipped = not (temp_board.turn == chess.BLACK)

        bg_color = "#f0f0f0"
        active_bg = "#d1e3ff"
        active_fg = "#1565c0"
        num_fg = "#999999"

        for i, move in enumerate(self.solution_moves):
            # Check whose turn it is BEFORE pushing the move
            is_white_turn = (temp_board.turn == chess.BLACK)
            full_move_number = temp_board.fullmove_number
            move_idx = i + 1

            # 1. Add Move Number
            # If White is to move, we show "1."
            # If Black is to move and it's the very first move of the list, we show "1..."
            if is_white_turn:
                num_text = f"{full_move_number}."
                num_lbl = tk.Label(self.move_text_container, text=num_text,
                                   font=("Consolas", 10), fg=num_fg, bg=bg_color)
                self.move_text_container.window_create(tk.END, window=num_lbl)
                self.move_text_container.insert(tk.END, " ")
            elif i == 0:
                # First move is black: show "1..."
                num_text = f"{full_move_number}..."
                num_lbl = tk.Label(self.move_text_container, text=num_text,
                                   font=("Consolas", 10), fg=num_fg, bg=bg_color)
                self.move_text_container.window_create(tk.END, window=num_lbl)
                self.move_text_container.insert(tk.END, " ")

            # 2. Create the Move Label (using SAN from your list)
            san_text = self.san_list[i]
            lbl = tk.Label(self.move_text_container, text=san_text, font=("Consolas", 10),
                           fg="black", bg=bg_color, cursor="hand2")

            if move_idx == self.current_step:
                lbl.config(bg=active_bg, fg=active_fg, font=("Consolas", 10, "bold"))

            lbl.bind("<Button-1>", lambda e, idx=move_idx: self._jump_to_move(idx))

            # 3. Add to flow and push the move to the temp_board for the next iteration
            self.move_text_container.window_create(tk.END, window=lbl)
            self.move_text_container.insert(tk.END, "  ")

            temp_board.push(move)

        self.move_text_container.config(state=tk.DISABLED)

    def _animate_piece(self, from_sq, to_sq, callback):
        """ Universal animation handler with an animation lock. """
        self.is_animating = True

        piece_id = self.drawn_pieces.get(from_sq)
        if not piece_id:
            self.is_animating = False
            callback()
            return

        def get_pos(sq):
            f, r = chess.square_file(sq), chess.square_rank(sq)
            col, row = (7 - f, r) if self.is_flipped else (f, 7 - r)
            return col * self.field_size, row * self.field_size

        start_x, start_y = get_pos(from_sq)
        target_x, target_y = get_pos(to_sq)
        self.canvas.tag_raise(piece_id)

        steps = 12
        dx = (target_x - start_x) / steps
        dy = (target_y - start_y) / steps

        def step(count):
            if count < steps:
                self.canvas.move(piece_id, dx, dy)
                self.after(12, lambda: step(count + 1))
            else:
                self.is_animating = False
                callback()

        step(0)

    def _jump_to_move(self, index):
        """
        Jumps to a specific move index, intelligently choosing between
        forward animation, backward animation, or a static jump.
        """
        if self.animator.is_animating:
            return

        # We want to animate the move that leads TO this index.
        # If index is 5, we animate move 4 (0-indexed) from step 4 to 5.
        target_step_pre = index - 1

        # 1. Handle jump to the very beginning (no animation)
        if index <= 0:
            while len(self.review_board.move_stack) > 0:
                self.review_board.pop()
            self.current_step = 0
            self.last_move_squares = []
            self._update_display()
            return

        # 2. Navigate the board to the 'pre-animation' state
        # We use push/pop to get to the state exactly before the move we want to animate.
        diff = target_step_pre - self.current_step
        if diff > 0:
            for i in range(diff):
                self.review_board.push(self.solution_moves[self.current_step + i])
        elif diff < 0:
            for _ in range(abs(diff)):
                self.review_board.pop()

        self.current_step = target_step_pre
        self.refresh_board()  # Show the piece at its starting position

        # 3. Determine animation direction
        # If we are going to a higher index than where we were, it's a forward move.
        # If we are 'jumping back' (e.g., from move 10 to move 5), we animate the move at index 5 returning.
        move = self.solution_moves[index - 1]

        # Logic for forward vs backward animation
        # Note: Usually, for a 'jump' back, users expect to see the move being undone.
        is_reverse = (index <= self.current_step)

        def finalize():
            # Finalize board state after animation
            if not is_reverse:
                self.review_board.push(move)
                self.current_step = index
            else:
                # If we were already past this move and jumped back,
                # the piece has 'returned' to its start.
                self.current_step = index
                # The board is already at the correct state (target_step_pre)
                # but we need to ensure the stack is correct if you'd push again.
                pass

            self.last_move_squares = [move.from_square, move.to_square]
            self._update_display()

        # 4. Execute animation
        self.animator.animate(
            move.from_square,
            move.to_square,
            callback=finalize,
            reverse=is_reverse
        )

    def _next_move(self):
        if self.current_step < len(self.solution_moves):
            self._jump_to_move(self.current_step + 1)

    def _prev_move(self):
        """ Moves back one step with a visual 'return' animation. """
        if self.animator.is_animating or self.current_step <= 0:
            return

        # The move we are undoing
        move = self.solution_moves[self.current_step - 1]

        def finalize_undo():
            self.review_board.pop()
            self.current_step -= 1
            # Update highlights for the move now at the top of the stack
            if self.current_step > 0:
                m = self.solution_moves[self.current_step - 1]
                self.last_move_squares = [m.from_square, m.to_square]
            else:
                self.last_move_squares = []
            self._update_display()

        # Animate from its CURRENT 'to_square' back to 'from_square'
        self.animator.animate(move.from_square, move.to_square,
                              callback=finalize_undo, reverse=True)

    def refresh_board(self):
        if self.is_animating:
            return
        self.canvas.delete("all")
        size = self.field_size
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
        self.drawn_pieces = {}
        for square, piece in self.review_board.piece_map().items():
            f, r = chess.square_file(square), chess.square_rank(square)
            col, row = (7 - f, r) if self.is_flipped else (f, 7 - r)
            #print(f"Drawing {piece.symbol()} at {square}")
            img = self.piece_images.get(piece.symbol())
            if img:
                piece_id = self.canvas.create_image(col * size, row * size, image=img, anchor=tk.NW, tags=("piece",))
                self.drawn_pieces[square] = piece_id


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
                                board_theme=self.parent.board_theme, themes=self.parent.themes, piece_set=self.piece_set,
                                config=self.parent.config_data)


class AnalysisWindow(tk.Toplevel):
    def __init__(self, parent, stats):
        super().__init__(parent)
        # Assuming parent has access to the translation method
        self.t = parent.t
        self.parent = parent

        self.title(self.t("analysis_title"))
        self.geometry("450x600")
        self.configure(bg="#f8f9fa")

        # Main Title
        tk.Label(self, text=self.t("db_overview"), font=("Segoe UI", 16, "bold"),
                 bg="#f8f9fa", fg="#2c3e50").pack(pady=20)
        self._add_validation_section(stats)
        # Statistics Summary Card
        card = tk.Frame(self, bg="white", padx=20, pady=20, relief=tk.SOLID, borderwidth=1)
        card.pack(fill=tk.X, padx=30)

        # Helper to create stats rows
        self._add_stat_row(card, self.t("total_puzzles"), stats['total'])
        self._add_stat_row(card, self.t("rating_range"), f"{stats['min_rating']} - {stats['max_rating']}")
        self._add_stat_row(card, self.t("avg_rating"), stats['avg_rating'])

        # Themes Section
        tk.Label(self, text=self.t("top_themes"), font=("Segoe UI", 12, "bold"),
                 bg="#f8f9fa", fg="#2c3e50").pack(pady=(25, 10))

        # 1. Create a container frame for the Canvas and Scrollbar
        container = tk.Frame(self, bg="white", relief=tk.SOLID, borderwidth=1)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=5)

        # 2. Create the Canvas
        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        # 3. This is the frame that will actually hold the themes
        scrollable_frame = tk.Frame(canvas, bg="white")

        # Configure the canvas to work with the scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Place the frame inside the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=370)  # Set width to match your UI
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack Canvas and Scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 4. Fill the scrollable_frame with themes
        # Loop through themes and make them interactive
        for theme, count in stats['themes'].items():
            # Create a frame that acts as a button
            row = tk.Frame(scrollable_frame, bg="white", cursor="hand2")
            row.pack(fill=tk.X, pady=3, padx=10)

            trans_key = theme.lower().replace(" ", "_")
            display_theme = self.t(trans_key) or theme

            # Create the labels inside the frame
            lbl_name = tk.Label(row, text=display_theme, bg="white", fg="#7f8c8d", cursor="hand2")
            lbl_name.pack(side=tk.LEFT)

            lbl_count = tk.Label(row, text=str(count), bg="white", font=("Segoe UI", 10, "bold"),
                                 fg="#2980b9", cursor="hand2")
            lbl_count.pack(side=tk.RIGHT)

            # Bind the click event to the frame and its children
            for widget in (row, lbl_name, lbl_count):
                widget.bind("<Button-1>", lambda e, t=theme: self._on_theme_click(t))

            # Optional hover effect
            row.bind("<Enter>", lambda e, r=row: r.configure(bg="#f0f7ff"))
            row.bind("<Leave>", lambda e, r=row: r.configure(bg="white"))

        # 5. Enable mouse wheel scrolling for Chromebook touchpad
        def _on_mousewheel(event):
            # Standard Linux mouse wheel handling (Button 4/5 or delta)
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
            else:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/MacOS
        canvas.bind_all("<Button-4>", _on_mousewheel)  # Linux (Ubuntu)
        canvas.bind_all("<Button-5>", _on_mousewheel)  # Linux (Ubuntu)
        # Close button at bottom
        ttk.Button(self, text=self.t("close"), command=self.destroy).pack(pady=25)

    def _on_theme_click(self, theme_name):
        """
        Handles the click event on a theme.
        Filters the puzzle list and starts the first matching puzzle.
        """
        # Tell the engine to filter puzzles by this theme
        # We assume your engine has a method for this, or we do it here:
        filtered = [p for p in self.parent.engine.puzzles if theme_name in p.get('themes', '')]

        if filtered:
            # Logic to update the main app's current puzzle set
            # For example, you could trigger a search in your main window:
            self.parent.apply_filter(theme_name)  # You would need to create this method
            self.destroy()  # Close the analysis window

    def _add_stat_row(self, parent, label, value):
        """ Internal helper to render a key-value pair in the UI. """
        row = tk.Frame(parent, bg="white")
        row.pack(fill=tk.X, pady=5)
        tk.Label(row, text=f"{label}:", bg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        tk.Label(row, text=str(value), bg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.RIGHT)

    def _add_validation_section(self, stats):
        """ Adds a button to trigger the puzzle validation tool. """
        tk.Label(self, text=self.t("maintenance"), font=("Segoe UI", 12, "bold"),
                 bg="#f8f9fa", fg="#2c3e50").pack(pady=(20, 5))

        self.btn_validate = ttk.Button(
            self,
            text=self.t("run_validation"),
            command=self._run_integrity_check
        )
        self.btn_validate.pack(pady=10)

    def _run_integrity_check(self):
        """ Executes the PuzzleValidator and shows results. """
        # parent.engine contains the puzzles list
        validator = PuzzleValidator(self.parent.engine.puzzles)
        errors = validator.validate_all()

        if not errors:
            messagebox.showinfo(self.t("validation_result"), self.t("all_puzzles_valid"))
        else:
            # Show errors in a simple scrollable list or separate window
            error_msg = "\n".join([f"#{e['index']} ({e['name']}): {e['reason']}" for e in errors[:10]])
            if len(errors) > 10:
                error_msg += f"\n... and {len(errors) - 10} more."

            messagebox.showwarning(self.t("validation_result"),
                                   f"{self.t('errors_found')}: {len(errors)}\n\n{error_msg}")


class OverallProgressWindow(tk.Toplevel):
    def __init__(self, parent, stats):
        super().__init__(parent)
        self.parent = parent
        self.t = parent.t

        self.title(self.t("overall_progress_title"))
        self.geometry("750x700")
        self.configure(bg="#f8f9fa")

        # --- Summary Header ---
        summary_bg = "#2c3e50"
        summary_frame = tk.Frame(self, bg=summary_bg, pady=25)
        summary_frame.pack(fill=tk.X)

        # Display global metrics
        tk.Label(summary_frame, text=self.t("overall_performance"),
                 bg=summary_bg, fg="#bdc3c7", font=("Segoe UI", 11)).pack()

        score_text = f"{self.t('total_score')}: {stats['total_score']} | {stats['total_solved']} {self.t('puzzles_solved')}"
        tk.Label(summary_frame, text=score_text,
                 bg=summary_bg, fg="#2ecc71", font=("Segoe UI", 16, "bold")).pack(pady=5)

        # --- List Header ---
        header_frame = tk.Frame(self, bg="#dfe6e9", padx=20, pady=10)
        header_frame.pack(fill=tk.X, pady=(15, 0))

        tk.Label(header_frame, text=self.t("file_url"), width=40, anchor="w", bg="#dfe6e9",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        tk.Label(header_frame, text=self.t("score"), width=12, anchor="e", bg="#dfe6e9",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.RIGHT)
        tk.Label(header_frame, text=self.t("file_size"), width=15, anchor="e", bg="#dfe6e9",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.RIGHT)

        # --- Scrollable Area ---
        container = tk.Frame(self, bg="white")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview, style="Thick.Vertical.TScrollbar")
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_win = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_win, width=e.width))

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for f in stats['files']:
            row = tk.Frame(scroll_frame, bg="white", pady=15)
            row.pack(fill=tk.X)

            # Left side - File details
            info_frame = tk.Frame(row, bg="white")
            info_frame.pack(side=tk.LEFT, padx=10)
            tk.Label(info_frame, text=f['name'], bg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w")

            short_path = (f['full_path'][-50:] if len(f['full_path']) > 50 else f['full_path'])
            tk.Label(info_frame, text=short_path, bg="white", font=("Consolas", 8), fg="#7f8c8d").pack(anchor="w")

            # Right side - Metrics
            tk.Label(row, text=f"{f['score']} pts", width=12, anchor="e", bg="white", fg="#2980b9",
                     font=("Segoe UI", 10, "bold")).pack(side=tk.RIGHT, padx=5)

            # Display size in MB
            size_txt = f"{f['size_mb']:.2f} MB"
            tk.Label(row, text=size_txt, width=12, anchor="e", bg="white", fg="#7f8c8d").pack(side=tk.RIGHT, padx=5)

            # Solved count as a small badge
            tk.Label(row, text=f"✓ {f['solved']}", bg="#e8f5e9", fg="#2e7d32", padx=5).pack(side=tk.RIGHT, padx=10)

            tk.Frame(scroll_frame, height=1, bg="#f1f2f6").pack(fill=tk.X)

        # Standard mousewheel binding
        def _on_mousewheel(event):
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
            else:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

        ttk.Button(self, text=self.t("close"), command=self.destroy).pack(pady=20)

class ProgressWindow(tk.Toplevel):
    def __init__(self, parent, results_log):
        super().__init__(parent)
        self.parent = parent
        self.title(self.parent.t("progress"))
        # Reduced height from 550 to 500 to remove dead space
        self.geometry("900x500")

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
        self.drawn_pieces = {}
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
        self.animator = MoveAnimator(self)

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

        # English: Dynamically generate menu items based on the TRANSLATIONS dictionary
        # 'code' will be "en", "nl", etc.
        # 'content' will be the inner dictionary containing "lang_name"
        for code, content in TRANSLATIONS.items():
            # English: Use the "lang_name" defined in the dictionary for the label
            display_name = content.get("lang_name", code)

            # English: Bind the command to set the language
            lang_m.add_command(
                label=display_name,
                command=lambda c=code: self._set_lang(c)
            )
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

        # Submenu for Piece Sets
        pieces_m = tk.Menu(settings_m, tearoff=0)
        settings_m.add_cascade(label=t("piece_set"), menu=pieces_m)

        # List available sets manually (or scan the Images folder)
        available_sets = ["tatiana", "staunty"]

        for p_set in available_sets:
            # capitalize() makes the menu look cleaner (e.g., 'Staunty')
            pieces_m.add_command(
                label=p_set.capitalize(),
                command=lambda s=p_set: self._set_piece_set(s)
            )

        # Submenu for Board Size
        size_m = tk.Menu(settings_m, tearoff=0)
        settings_m.add_cascade(label=t("board_size"), menu=size_m)

        # Mapping display keys to pixel values
        sizes = [
            ("small", 60),
            ("medium", 70),
            ("large", 77),
            ("extra_large", 84),
            ("huge", 90)
        ]

        for key, val in sizes:
            # We use l=val to capture the current size in the loop
            size_m.add_command(
                label=t(key),
                command=lambda v=val: self._set_field_size(v)
            )
        # Orientation Submenu
        orient_m = tk.Menu(settings_m, tearoff=0)
        settings_m.add_cascade(label=t("orientation"), menu=orient_m)
        orient_m.add_command(label=t("portrait"), command=lambda: self._set_orientation("portrait"))
        orient_m.add_command(label=t("landscape"), command=lambda: self._set_orientation("landscape"))

        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.t("view"), menu=view_menu)
        view_menu.add_command(label=self.t("history"), command=lambda: HistoryWindow(self, self.engine, piece_set=self.piece_set))
        view_menu.add_command(label=self.t("progress"), command=lambda: ProgressWindow(self, self.engine.results_log))
        view_menu.add_command(label=self.t("analyze_db"), command=self._show_db_analysis)
        view_menu.add_command(label=self.t("menu_filter"), command=self._open_filter_window)
        view_menu.add_command(label=self.t("overall_progress_title"), command=self._show_overall_progress)

        view_menu.add_separator()
        view_menu.add_command(label=self.t("reset"), command=self._confirm_reset)

    def _setup_ui(self):
        # The very outer background (visible during transitions)
        self.config(bg="#dcdcdc")

        # The light border frame around the entire app
        self.master_container = tk.Frame(self, bg="#f0f0f0", bd=2, relief=tk.FLAT)

        # Sidebar/Header (we will style this in _arrange_layout)
        self.header = tk.Frame(self.master_container, pady=20, padx=20)

        # Labels inside the header
        self.lbl_rating = tk.Label(self.header, text="", font=("Segoe UI", 10, "bold"))
        self.lbl_overall = tk.Label(self.header, text="", font=("Segoe UI", 10))
        self.lbl_overall.pack()
        self.lbl_event = tk.Label(self.header, text="", font=("Segoe UI", 12, "bold"))
        self.lbl_event.pack()
        self.lbl_sub = tk.Label(self.header, text="", font=("Segoe UI", 9, "italic"))
        self.lbl_sub.pack()

        # The "Black Badge" Turn Indicator
        self.turn_badge = tk.Frame(self.header, padx=15, pady=8, relief=tk.RAISED, bd=2)
        self.lbl_turn = tk.Label(self.turn_badge, text="", font=("Segoe UI", 11, "bold"))
        self.lbl_turn.pack()

        # Styled Turn Indicator (The "Badge")
        # We put it in a frame to give it a nice border/background
        self.turn_badge = tk.Frame(self.header, padx=10, pady=5, relief=tk.RAISED, bd=1)
        self.turn_badge.pack(pady=20)

        self.lbl_turn = tk.Label(self.turn_badge, text="", font=("Segoe UI", 11, "bold"))
        self.lbl_turn.pack()

        # 2. Board Container (The frame that holds both the board and the buttons)
        # Important: We don't pack it here, _arrange_layout will do that.
        self.board_container = tk.Frame(self.master_container, bg="#f0f0f0")

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
        self._arrange_layout()

    def _set_orientation(self, mode):
        """ Updates orientation, saves to config and rearranges the UI. """
        self.config_data["orientation"] = mode
        self._save_config()
        self._arrange_layout()

    def _arrange_layout(self):
        """ Restores the dashboard look with a protective outer border. """
        self.header.pack_forget()
        self.board_container.pack_forget()
        self.master_container.pack_forget()

        orientation = self.config_data.get("orientation", "portrait")
        bg_frame = self.current_theme.get("frame", "#f7f7f7")
        board_px = (self.field_size * 8) + 50

        if orientation == "portrait":
            # Use very small paddings (pady) to save vertical space
            content_w = board_px + 40
            content_h = board_px + 180  # Reduced height estimate

            self.header.config(bg="#f0f0f0", pady=2)  # Minimal padding for the header frame

            # Stack labels with 0 or 1 pixel padding
            self.lbl_rating.config(bg="#f0f0f0", fg="#555555")
            self.lbl_rating.pack(side=tk.TOP, pady=0)
            self.lbl_overall.pack(side=tk.TOP, pady=0)
            self.lbl_event.pack(side=tk.TOP, pady=0)
            self.lbl_sub.pack(side=tk.TOP, pady=0)

            # The badge gets just enough space to not touch the text
            self.turn_badge.config(bg="#333333", bd=1, relief=tk.SOLID)
            self.turn_badge.pack(side=tk.TOP, pady=4)
            self.lbl_turn.config(bg="#333333", fg="white", font=("Segoe UI", 9, "bold"))

            # Colors for portrait
            for lbl in [self.lbl_overall, self.lbl_event, self.lbl_sub]:
                lbl.config(bg="#f0f0f0", fg="black")

            self.header.pack(side=tk.TOP, fill=tk.X)
            self.board_container.pack(side=tk.TOP, pady=2)
        else:
            # 2. LANDSCAPE (Grey Board Area vs Dark Sidebar)
            sidebar_w = 350
            content_w = board_px + sidebar_w + 20
            content_h = board_px + 80

            # Sidebar stays dark/wood-toned
            self.header.config(bg=bg_frame, pady=30)

            # Board container becomes grey to create a visual break
            bg_grey = "#e0e0e0"  # A clean, neutral grey
            self.board_container.config(bg=bg_grey)
            self.controls_under_board.config(bg=bg_grey)

            # Styles for labels in their respective areas
            for lbl in [self.lbl_overall, self.lbl_event, self.lbl_sub]:
                lbl.config(bg=bg_frame, fg="white")

            self.lbl_attempts.config(bg=bg_grey, fg="black")  # Counter on grey needs dark text

            # Dashboard spacing
            self.lbl_rating.config(bg=bg_frame, fg="#ffcc00")  # Gold color for rating looks great on dark
            self.lbl_rating.pack(side=tk.TOP, pady=5)
            self.lbl_overall.pack(side=tk.TOP, pady=(20, 10))
            self.lbl_event.pack(side=tk.TOP, pady=10)
            self.lbl_sub.pack(side=tk.TOP, pady=10)
            self.turn_badge.pack(side=tk.TOP, pady=30)

            # Pack with distinct zones
            self.board_container.pack(side=tk.LEFT, fill=tk.Y, padx=(1, 0))
            self.header.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Final assembly with a very thin white margin
        self.master_container.config(width=content_w, height=content_h)
        self.master_container.pack(expand=True, padx=5, pady=5)

        self._update_window_size(content_w + 10, content_h + 10)
        self.update()

    def _update_window_size(self, content_w, content_h):
        """
        Adjusts the physical window geometry based on the calculated content size.
        Includes extra padding for the 'border frame' effect.
        """
        # Add extra padding for the master_container margins (e.g., 40px total)
        total_w = content_w + 40
        total_h = content_h + 40

        # Get screen dimensions to prevent the window from being larger than the display
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        # Ensure we don't exceed screen limits (important for Chromebooks)
        final_w = min(total_w, screen_w - 50)
        final_h = min(total_h, screen_h - 100)

        # Update geometry only if not in a 'zoomed' or 'fullscreen' state
        # to avoid the "double title bar" glitch on ChromeOS.
        state = self.wm_state()
        if state != "zoomed" and not self.attributes("-fullscreen"):
            self.geometry(f"{int(final_w)}x{int(final_h)}")

        # Center the window on the screen for a professional look
        # (Optional: only if you want the window to jump to the middle)
        # x = (screen_w // 2) - (final_w // 2)
        # y = (screen_h // 2) - (final_h // 2)
        # self.geometry(f"+{int(x)}+{int(y)}")

        self.update()  # Force the window manager to apply changes immediately

    def _set_field_size(self, size):
        """ Updates the field size, reloads images at the new scale, and resizes the board. """
        self.field_size = size
        self.config_data["field_size"] = size
        self._save_config()

        # We must reload images because they need to be re-scaled to the new size
        self._load_images(size)

        # Update the canvas size and refresh everything
        canvas_width = size * 8
        self.canvas.config(width=canvas_width, height=canvas_width)
        self.refresh_board()

    def _open_filter_window(self):
        """
        Calculates current database statistics and opens the filter window.
        """
        # Generate stats to get the list of available themes and rating ranges
        stats = self.engine.analyze_database()

        # Open the window and pass the stats object
        FilterWindow(self, stats)

    def _show_overall_progress(self):
        """
        Triggers data collection and shows the overall progress dashboard.
        """
        # Collect data via the engine
        stats = self.engine.get_overall_progress_data(self.config_data)
        # Open the newly named window
        OverallProgressWindow(self, stats)

    def _show_db_analysis(self):
        """
        Triggers the database analysis and opens the stats window.
        """
        # Ensure puzzles are loaded before analyzing
        if not self.engine.puzzles:
            messagebox.showinfo(self.t("info"), self.t("no_puzzles_loaded"))
            return
        stats = self.engine.analyze_database()
        # AnalysisWindow is the class we defined in the previous step
        AnalysisWindow(self, stats)

    def apply_filter(self, theme_query):
        """
        Updates the active puzzle list based on a theme and resets the view.
        """
        # Filter the engine's list
        new_selection = [p for p in self.engine.puzzles if theme_query.lower() in p.get('themes', '').lower()]

        if new_selection:
            # Update your app's current list and load the first one
            self.engine.current_selection = new_selection
            self.load_puzzle()
            messagebox.showinfo(self.t("info"), f"{len(new_selection)} {self.t('puzzles_found')}")

    def _setup_lang_menu(self, parent_menu, translator):
        """ Dynamically builds the language selection menu. """
        lang_menu = tk.Menu(parent_menu, tearoff=0)
        parent_menu.add_cascade(label=translator("language"), menu=lang_menu)

        # Loop through available languages from the translator object
        # for code, name in translator.get_available_languages():
        #     # We use 'l=code' in the lambda to capture the current value of code
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

        # Reload the images with the new set
        self._load_images(self.field_size)

        # Refresh the board to show new pieces
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
        self._arrange_layout()

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
        self.drawn_pieces = {}
        if has_board:
            for sq, pc in self.board.piece_map().items():
                f, r = chess.square_file(sq), chess.square_rank(sq)
                col, row = (7 - f, r) if self.is_flipped else (f, 7 - r)
                img = self.piece_images.get(pc.symbol())
                if img:
                    piece_id =self.canvas.create_image(col * size, row * size, image=img, anchor=tk.NW, tags=("piece",))
                    self.drawn_pieces[sq] = piece_id

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
        puzzle_data = puzzle
        # 1. Try standard Elo tags first
        white_elo = puzzle_data.get("WhiteElo", "")
        black_elo = puzzle_data.get("BlackElo", "")

        rating = ""
        if white_elo and white_elo != "?":
            rating = f"Rating: {white_elo}"
        elif black_elo and black_elo != "?":
            rating = f"Rating: {black_elo}"
        else:
            # 2. Fallback: Scan player names for patterns like "(2121)"
            # This regex looks for digits inside parentheses
            pattern = r"\((\d+)\)"

            white_name = puzzle_data.get("white", "")
            black_name = puzzle_data.get("black", "")

            # Check White name first, then Black
            match_w = re.search(pattern, white_name)
            match_b = re.search(pattern, black_name)

            if match_w:
                rating = f"Rating: {match_w.group(1)}"
            elif match_b:
                rating = f"Rating: {match_b.group(1)}"

        # 3. Update the display
        if rating:
            self.lbl_rating.config(text=rating)
            # Ensure it is visible and placed correctly
            self.lbl_rating.pack(before=self.lbl_sub,
                                 pady=2 if self.config_data.get("orientation") == "portrait" else 5)
        else:
            # Hide the label if no rating is found to save space
            self.lbl_rating.pack_forget()

        if puzzle['initial_move']:
            self.board.push(puzzle['initial_move'])
            self.last_move_squares = [puzzle['initial_move'].from_square, puzzle['initial_move'].to_square]
        else:
            self.last_move_squares = []

        self.is_flipped = (self.board.turn == chess.BLACK)
        puzzle['is_flipped'] = self.is_flipped
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
        review = HistoryDetailWindow(self, p, result_score, t=self.t, board_theme=self.board_theme, themes=self.themes,
                                     piece_set=self.piece_set, remarks=remarks, config=self.config_data)
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
            self._handle_move(move, self.selected_square, sq)
            self.selected_square = None
            #self.refresh_board()

    def _handle_move(self, move, from_sq, to_sq):
        """
        Called when the user makes a move.
        Now animates correct moves before updating the board state.
        """
        if not self.engine or not self.board or self.animator.is_animating:
            return

        p = self.engine.puzzles[self.engine.current_index]

        # 1. Check if move is correct
        if move == p['solution'][self.solve_step]:

            # Define what happens AFTER the user's piece has finished sliding
            def finish_user_move():
                self.btn_hint.pack_forget()
                self.hint_square = None
                self.board.push(move)
                self.last_move_squares = [move.from_square, move.to_square]
                self.solve_step += 1

                if self.solve_step >= len(p['solution']):
                    # Puzzle solved logic
                    result = {3: 10, 2: 5, 1: 2}.get(self.attempts_left, 0)
                    self.engine.total_score += result
                    self._show_solution_and_continue(result, self.t("solved"))
                else:
                    # Wait a bit, then animate the opponent's reply
                    self.after(500, lambda: self._opp_move(p['solution'][self.solve_step]))

                self.refresh_board()

            # 2. Start the animation for the correct move
            # We use a fast delay (15-20ms) so the game feels responsive
            self.animator.animate(from_sq, to_sq, callback=finish_user_move)

        else:
            # 3. Handle Wrong Move (remains mostly the same)
            self.attempts_left -= 1
            self.btn_hint.pack(side=tk.LEFT, padx=5)

            if self.attempts_left <= 0:
                self._show_solution_and_continue(0, self.t("out_of_attempts"))
            else:
                # Fly back animation
                self._animate_wrong_move(from_sq, to_sq)
                self.lbl_attempts.config(text=f"Tries: {self.attempts_left}", fg="red")
                self.after(500, lambda: self.lbl_attempts.config(fg=self.themes[self.board_theme]["alert"]))

    def _animate_wrong_move(self, from_sq, to_sq):
        """
        Animates the piece moving from the 'wrong' square back to the 'start'
        using the MoveAnimator class.
        """
        # Prevent multiple simultaneous animations
        if self.animator.is_animating:
            return

        # We use a slower delay (40-60ms) for mistakes to make it more visible,
        # and a callback to refresh the board when finished.
        self.animator.animate(
            from_sq=to_sq,
            to_sq=from_sq,
            callback=self.refresh_board,
            reverse=True,
            steps=10,
            delay=40
        )

    def _opp_move(self, move):
        """
        Executes the opponent's move with a smooth forward animation.
        All comments are in English as requested.
        """
        # Guard against multiple animations
        if self.animator.is_animating:
            return

        def finish_opp():
            # Update the logic board state
            self.board.push(move)
            # Highlight the squares for the opponent's move
            self.last_move_squares = [move.from_square, move.to_square]
            # Increment the internal step counter
            self.solve_step += 1
            # Final UI sync
            self.refresh_board()

        # Use the MoveAnimator for a forward move (reverse=False)
        # A delay of 20-30ms is usually perfect for opponent responses.
        self.animator.animate(
            from_sq=move.from_square,
            to_sq=move.to_square,
            callback=finish_opp,
            reverse=False,
            steps=10,
            delay=25
        )

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

    def apply_advanced_filter(self, criteria):
        """
        Filters the puzzle database based on theme and rating checkboxes.
        """
        filtered_list = []

        for p in self.engine.puzzles:
            # Initial assumption is that the puzzle matches
            rating_ok = True
            theme_ok = True

            # 1. Handle Rating Filter if checkbox is active
            if criteria.get('use_rating'):
                try:
                    # Ensure we compare integers
                    puzzle_rating = int(p.get('rating', 0))
                    rating_ok = criteria['min_rating'] <= puzzle_rating <= criteria['max_rating']
                except (ValueError, TypeError):
                    rating_ok = False

            # 2. Handle Theme Filter if checkbox is active
            if criteria.get('use_theme'):
                selected_theme = criteria.get('theme', '').lower()
                puzzle_themes = p.get('themes', '').lower()
                theme_ok = selected_theme in puzzle_themes

            # Only add to selection if both conditions are met
            if rating_ok and theme_ok:
                filtered_list.append(p)

        # 3. Update the UI and selection
        if filtered_list:
            self.engine.current_selection = filtered_list
            self.load_puzzle()
            # Inform user about the results
            msg = f"{len(filtered_list)} {self.t('puzzles_found')}"
            messagebox.showinfo(self.t("info"), msg)
        else:
            messagebox.showwarning(self.t("info"), self.t("no_puzzles_found"))

    def reset_database_filter(self):
            """
            Restores the engine's current selection to the full puzzle list.
            """
            if hasattr(self.engine, 'puzzles'):
                self.engine.current_selection = list(self.engine.puzzles)
                self.load_puzzle()
                messagebox.showinfo(self.t("info"), self.t("filter_removed_msg"))



    def _on_close(self):
        self.engine.save_state()
        self._save_config()
        self.master.destroy()


# main call
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default=None)  # Default is now None
    args = parser.parse_args()

    root = tk.Tk()
    root.withdraw()

    # Always start the app, even if args.filename is None
    app = ChessPuzzleApp(args.filename)
    root.mainloop()
