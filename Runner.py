import pygame
import random
import sys

# Initialisation Pygame
pygame.init()
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tusmo - 3 Manches")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (100, 100, 255)

# Polices
font_large = pygame.font.SysFont('Arial', 50)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

# Paramètres du jeu
WORD_LENGTH = 5
MAX_ATTEMPTS = 6
words = ["ARBRE", "TABLE", "CHAIR", "FRUIT", "MAISON",
         "JOUET", "FLEUR", "VERRE", "TIGRE", "POULE"]


def new_game():
    global current_attempt, current_letter, game_over, secret_word, grid, colors
    current_attempt = 0
    current_letter = 0
    game_over = False
    secret_word = random.choice(words)
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
    global current_attempt, game_over, victories

    temp_secret = list(secret_word)
    result = [GRAY] * WORD_LENGTH

    # Lettres bien placées (vert)
    for i in range(WORD_LENGTH):
        if guess[i] == secret_word[i]:
            result[i] = GREEN
            temp_secret[i] = None

    # Lettres mal placées (jaune)
    for i in range(WORD_LENGTH):
        if result[i] == GRAY and guess[i] in temp_secret:
            result[i] = YELLOW
            temp_secret[temp_secret.index(guess[i])] = None

    colors[current_attempt] = result

    if guess == secret_word:
        game_over = True
        return True
    elif current_attempt == MAX_ATTEMPTS - 1:
        game_over = True

    current_attempt += 1
    current_letter = 0
    return False


# Boucle principale
def main():
    global current_letter, current_attempt

    victories = 0
    for manche in range(1, 4):
        new_game()
        running = True

        while running:
            screen.fill(WHITE)

            # Affichage manche en cours
            manche_text = font_small.render(f"Manche {manche}/3 - Victoires: {victories}", True, BLUE)
            screen.blit(manche_text, (20, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and current_letter == WORD_LENGTH:
                            guess = ''.join(grid[current_attempt])
                            if guess in words:
                                if check_guess(guess):
                                    victories += 1
                            else:
                                # Message mot invalide
                                pass

                        elif event.key == pygame.K_BACKSPACE and current_letter > 0:
                            current_letter -= 1
                            grid[current_attempt][current_letter] = ''

                        elif event.unicode.isalpha() and current_letter < WORD_LENGTH:
                            grid[current_attempt][current_letter] = event.unicode.upper()
                            current_letter += 1

            draw_grid()

            if game_over:
                if ''.join(grid[current_attempt]) == secret_word:
                    msg = "Gagné! Appuyez sur ESPACE pour continuer"
                else:
                    msg = f"Perdu! Mot: {secret_word}. ESPACE pour continuer"

                text = font_medium.render(msg, True, BLACK)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    break

            pygame.display.flip()

    # Ecran final
    screen.fill(WHITE)
    if victories == 3:
        msg = "Bravo! Vous avez gagné les 3 manches!"
    else:
        msg = f"Fin du jeu! Vous avez gagné {victories}/3 manches"

    text = font_medium.render(msg, True, BLUE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()