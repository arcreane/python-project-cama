import pygame
import random
import sys
from collections import defaultdict

# Initialisation Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tusmo-like Game")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Polices
font_large = pygame.font.SysFont('Arial', 50)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

# Paramètres du jeu
WORD_LENGTH = 5
MAX_ATTEMPTS = 6
current_row = 0
current_col = 0
game_over = False
victory = False

# Charger les mots (liste simplifiée pour l'exemple)
words = [
    "ARBRE", "TABLE", "CHAIR", "FRUIT", "MAISON",
    "SOLEIL", "FLEUR", "JARDIN", "MONTRE", "CARTE"
]
secret_word = random.choice(words)

# Grille de jeu
grid = [['' for _ in range(WORD_LENGTH)] for _ in range(MAX_ATTEMPTS)]
colors = [[WHITE for _ in range(WORD_LENGTH)] for _ in range(MAX_ATTEMPTS)]
key_colors = {letter: GRAY for letter in 'AZERTYUIOPQSDFGHJKLMWXCVBN'}

# Clavier
keyboard_rows = [
    'AZERTYUIOP',
    'QSDFGHJKLM',
    'WXCVBN'
]


def draw_grid():
    cell_size = 60
    margin = 10
    start_x = (WIDTH - (WORD_LENGTH * (cell_size + margin))) // 2
    start_y = 50

    for row in range(MAX_ATTEMPTS):
        for col in range(WORD_LENGTH):
            x = start_x + col * (cell_size + margin)
            y = start_y + row * (cell_size + margin)

            pygame.draw.rect(screen, colors[row][col], (x, y, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size), 2)

            if grid[row][col]:
                text_color = WHITE if colors[row][col] != WHITE else BLACK
                text = font_large.render(grid[row][col], True, text_color)
                text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
                screen.blit(text, text_rect)


def draw_keyboard():
    key_width = 40
    key_height = 50
    margin = 5
    start_y = HEIGHT - 180

    for row_idx, row in enumerate(keyboard_rows):
        start_x = (WIDTH - (len(row) * (key_width + margin))) // 2

        for col_idx, key in enumerate(row):
            x = start_x + col_idx * (key_width + margin)
            y = start_y + row_idx * (key_height + margin)

            pygame.draw.rect(screen, key_colors[key], (x, y, key_width, key_height))
            pygame.draw.rect(screen, BLACK, (x, y, key_width, key_height), 2)

            text_color = WHITE if key_colors[key] != GRAY else BLACK
            text = font_small.render(key, True, text_color)
            text_rect = text.get_rect(center=(x + key_width // 2, y + key_height // 2))
            screen.blit(text, text_rect)


def check_guess(guess):
    global current_row, game_over, victory, current_col

    temp_secret = list(secret_word)
    result = [GRAY] * WORD_LENGTH

    # Vérifier les lettres bien placées
    for i in range(WORD_LENGTH):
        if guess[i] == secret_word[i]:
            result[i] = GREEN
            temp_secret[i] = None
            key_colors[guess[i]] = GREEN

    # Vérifier les lettres mal placées
    for i in range(WORD_LENGTH):
        if result[i] == GRAY and guess[i] in temp_secret:
            result[i] = YELLOW
            temp_secret[temp_secret.index(guess[i])] = None
            if key_colors[guess[i]] != GREEN:
                key_colors[guess[i]] = YELLOW
        elif result[i] == GRAY:
            key_colors[guess[i]] = RED

    colors[current_row] = result

    if guess == secret_word:
        game_over = True
        victory = True
    elif current_row == MAX_ATTEMPTS - 1:
        game_over = True

    # Réinitialiser pour la prochaine ligne
    if not game_over:
        current_row += 1
        current_col = 0


# Boucle principale
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and current_col == WORD_LENGTH:
                    guess = ''.join(grid[current_row])
                    if guess in words:
                        check_guess(guess)
                    else:
                        # Message d'erreur temporaire
                        print("Mot invalide")

                elif event.key == pygame.K_BACKSPACE:
                    if current_col > 0:
                        current_col -= 1
                        grid[current_row][current_col] = ''

                elif event.unicode.isalpha() and current_col < WORD_LENGTH:
                    grid[current_row][current_col] = event.unicode.upper()
                    current_col += 1

    draw_grid()
    draw_keyboard()

    if game_over:
        if victory:
            message = "Gagné !"
        else:
            message = f"Perdu ! Le mot était {secret_word}"

        text = font_medium.render(message, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

pygame.quit()
sys.exit()