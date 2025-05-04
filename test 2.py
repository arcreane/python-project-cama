import pygame
import random
import sys

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

# Polices
font_large = pygame.font.SysFont('Arial', 50)
font_medium = pygame.font.SysFont('Arial', 36)

# Paramètres du jeu
WORD_LENGTH = 5
MAX_ATTEMPTS = 6
current_attempt = 0
current_letter = 0
game_over = False
secret_word = random.choice(["ARBRE", "TABLE", "CHAIR", "FRUIT", "MAISON"])
grid = [['' for _ in range(WORD_LENGTH)] for _ in range(MAX_ATTEMPTS)]
colors = [[WHITE for _ in range(WORD_LENGTH)] for _ in range(MAX_ATTEMPTS)]


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
                text_color = BLACK if colors[row][col] == WHITE else WHITE
                text = font_large.render(grid[row][col], True, text_color)
                text_rect = text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
                screen.blit(text, text_rect)


def check_guess(guess):
    global current_attempt, game_over

    # Créer une copie modifiable du mot secret
    temp_secret = list(secret_word)
    result = [GRAY] * WORD_LENGTH

    # D'abord vérifier les lettres bien placées (vert)
    for i in range(WORD_LENGTH):
        if guess[i] == secret_word[i]:
            result[i] = GREEN
            temp_secret[i] = None  # Marquer comme déjà trouvé

    # Ensuite vérifier les lettres mal placées (jaune)
    for i in range(WORD_LENGTH):
        if result[i] == GRAY and guess[i] in temp_secret:
            result[i] = YELLOW
            temp_secret[temp_secret.index(guess[i])] = None

    # Appliquer les couleurs à la ligne actuelle
    colors[current_attempt] = result

    # Vérifier si le joueur a gagné
    if guess == secret_word:
        game_over = True
        return True
    elif current_attempt == MAX_ATTEMPTS - 1:
        game_over = True
    else:
        current_attempt += 1
        current_letter = 0

    return False


# Boucle principale
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and current_letter == WORD_LENGTH:
                    guess = ''.join(grid[current_attempt])
                    if len(guess) == WORD_LENGTH:  # Validation simplifiée
                        check_guess(guess)

                elif event.key == pygame.K_BACKSPACE and current_letter > 0:
                    current_letter -= 1
                    grid[current_attempt][current_letter] = ''

                elif event.unicode.isalpha() and current_letter < WORD_LENGTH:
                    grid[current_attempt][current_letter] = event.unicode.upper()
                    current_letter += 1

    draw_grid()

    if game_over:
        message = "Bravo !" if ''.join(grid[current_attempt]) == secret_word else f"Perdu. Mot: {secret_word}"
        text = font_medium.render(message, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

pygame.quit()
sys.exit()