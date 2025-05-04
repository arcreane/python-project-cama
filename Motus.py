import pygame
import random
import sys
import string
from collections import defaultdict


# === Fonctions utilitaires ===
def charger_mots_par_longueur(fichier):
    try:
        mots_par_longueur = defaultdict(list)
        with open(fichier, encoding="utf-8") as f:
            for ligne in f:
                mot = ligne.strip().upper()
                if 4 <= len(mot) <= 9 and mot.isalpha():
                    mots_par_longueur[len(mot)].append(mot)
        return dict(mots_par_longueur)
    except FileNotFoundError:
        print(f"Erreur: Le fichier {fichier} est introuvable.")
        sys.exit(1)


def calculer_tailles_grille(cols, max_tile_size=70, margin_ratio=0.1):
    largeur_disponible = WIDTH - 100
    tile_size = min(max_tile_size, largeur_disponible // (cols + (cols - 1) * margin_ratio))
    margin = tile_size * margin_ratio
    return int(tile_size), int(margin)


def get_new_word():
    length = random.choice(list(WORDS_BY_LENGTH.keys()))
    return random.choice(WORDS_BY_LENGTH[length]).upper()


def check_word(word, word_list):
    return word.upper() in word_list


def evaluate_guess(guess, secret_word):
    temp_secret = list(secret_word)
    result_colors = [GREY] * len(secret_word)

    # D'abord vérifier les lettres bien placées (rouges)
    for i in range(len(secret_word)):
        if guess[i] == secret_word[i]:
            result_colors[i] = RED
            temp_secret[i] = None

    # Ensuite vérifier les lettres mal placées (jaunes)
    for i in range(len(secret_word)):
        if result_colors[i] == GREY and guess[i] in temp_secret:
            result_colors[i] = YELLOW
            temp_secret[temp_secret.index(guess[i])] = None

    return result_colors


def draw_grid(grid, colors, cols):
    TILE_SIZE, MARGIN = calculer_tailles_grille(cols)
    start_x = (WIDTH - (cols * TILE_SIZE + (cols - 1) * MARGIN)) // 2
    for row in range(ROWS):
        for col in range(cols):
            x = start_x + col * (TILE_SIZE + MARGIN)
            y = row * (TILE_SIZE + MARGIN) + TOP_MARGIN
            letter = grid[row][col]
            color = colors[row][col] if letter else WHITE
            pygame.draw.rect(SCREEN, color, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(SCREEN, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)
            if letter:
                text_color = BLACK if color == WHITE else WHITE
                text = FONT.render(letter, True, text_color)
                SCREEN.blit(text, (x + TILE_SIZE // 2 - text.get_width() // 2,
                                   y + TILE_SIZE // 2 - text.get_height() // 2))


def draw_message(text):
    label = FONT.render(text, True, BLACK)
    SCREEN.blit(label, (WIDTH // 2 - label.get_width() // 2, 30))


def draw_keyboard():
    key_width, key_height = 45, 55
    spacing = 8
    start_y = HEIGHT - 3 * (key_height + spacing) - 20
    keyboard_buttons.clear()

    for row_index, row in enumerate(KEYBOARD_LAYOUT):
        row_width = len(row) * (key_width + spacing) - spacing
        start_x = (WIDTH - row_width) // 2

        for i, key in enumerate(row):
            x = start_x + i * (key_width + spacing)
            y = start_y + row_index * (key_height + spacing)
            color = KEY_COLORS.get(key.upper(), WHITE)
            rect = pygame.Rect(x, y, key_width, key_height)
            pygame.draw.rect(SCREEN, color, rect)
            pygame.draw.rect(SCREEN, BLACK, rect, 2)
            text_color = BLACK if color == WHITE else WHITE
            text = SMALL_FONT.render(key.upper(), True, text_color)
            SCREEN.blit(text, (
                x + key_width // 2 - text.get_width() // 2,
                y + key_height // 2 - text.get_height() // 2
            ))
            keyboard_buttons[key.upper()] = rect


# === Initialisation pygame ===
pygame.init()
WIDTH, HEIGHT = 800, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MOTUS - 3 Manches")
FONT = pygame.font.SysFont("arial", 36)
SMALL_FONT = pygame.font.SysFont("arial", 24)

# === Constantes ===
TOP_MARGIN = 100
ROWS = 6
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
GREY = (169, 169, 169)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
KEYBOARD_LAYOUT = [list("AZERTYUIOP"), list("QSDFGHJKLM"), list("WXCVBN")]
KEY_COLORS = {letter: WHITE for letter in string.ascii_uppercase}
keyboard_buttons = {}

# === Chargement des mots ===
WORDS_BY_LENGTH = charger_mots_par_longueur("mots.txt")

# === Boucle de jeu principale ===
victories = 0
manche = 1
MAX_MANCHES = 3
game_running = True

while manche <= MAX_MANCHES and game_running:
    # Réinitialiser les couleurs du clavier pour chaque manche
    KEY_COLORS = {letter: WHITE for letter in string.ascii_uppercase}

    secret_word = get_new_word()
    cols = len(secret_word)
    words = WORDS_BY_LENGTH[cols]
    grid = [["" for _ in range(cols)] for _ in range(ROWS)]
    colors = [[WHITE for _ in range(cols)] for _ in range(ROWS)]
    current_row = 0
    current_col = 0
    message = ""
    manche_over = False

    while not manche_over and game_running:
        SCREEN.fill(WHITE)
        draw_grid(grid, colors, cols)
        draw_message(f"Manche {manche}/3 - {message}")
        draw_keyboard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if manche_over or not game_running:
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and current_col > 0:
                    current_col -= 1
                    grid[current_row][current_col] = ""

                elif event.key == pygame.K_RETURN:
                    guess = "".join(grid[current_row])
                    if len(guess) == cols:
                        if check_word(guess, words):
                            result_colors = evaluate_guess(guess, secret_word)
                            colors[current_row] = result_colors

                            # Mettre à jour les couleurs du clavier
                            for idx, letter in enumerate(guess):
                                color = result_colors[idx]
                                if color == RED:
                                    KEY_COLORS[letter] = RED
                                elif color == YELLOW and KEY_COLORS[letter] != RED:
                                    KEY_COLORS[letter] = YELLOW
                                elif color == GREY and KEY_COLORS[letter] not in (RED, YELLOW):
                                    KEY_COLORS[letter] = GREY

                            if guess == secret_word:
                                message = "GAGNÉ !"
                                victories += 1
                                manche_over = True
                            else:
                                current_row += 1
                                current_col = 0
                                if current_row == ROWS:
                                    message = f"PERDU ! Mot : {secret_word}"
                                    manche_over = True
                        else:
                            message = "Mot invalide"
                            # Ne pas avancer au rang suivant pour un mot invalide
                            # Marquer les lettres absentes en gris
                            for letter in guess:
                                if letter not in secret_word and KEY_COLORS[letter] == WHITE:
                                    KEY_COLORS[letter] = GREY

                elif event.unicode.isalpha() and current_col < cols:
                    grid[current_row][current_col] = event.unicode.upper()
                    current_col += 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for letter, rect in keyboard_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if len(letter) == 1 and current_col < cols:
                            grid[current_row][current_col] = letter
                            current_col += 1

        pygame.display.flip()

    pygame.time.delay(1500)
    manche += 1

# === Fin du jeu ===
SCREEN.fill(WHITE)
if victories == MAX_MANCHES:
    draw_message("🎉 Vous avez gagné les 3 manches !")
else:
    draw_message(f"Fin du jeu - {victories}/3 manches gagnées")
pygame.display.flip()
pygame.time.delay(3000)
pygame.quit()
sys.exit()