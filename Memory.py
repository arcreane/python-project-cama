import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
FONT = pygame.font.Font(pygame.font.match_font("segoeuisymbol", True ), 50)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mémo - Jeu de mémoire")

# Génération des symboles et du plateau
symbols = ["\u2605", "\u2600", "\u2601", "\u2660", "\u2666", "\u2764", "\u266B", "\u273F"] * 2 # 8 paires
random.shuffle(symbols)
grid = [symbols[i * GRID_SIZE:(i + 1) * GRID_SIZE] for i in range(GRID_SIZE)]
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]


# Affichage initial des symboles pendant 15 secondes
def show_initial_grid():
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            draw_tile(row, col, reveal=True)
    pygame.display.flip()
    time.sleep(10)


# Dessine une case
def draw_tile(row, col, reveal=False):
    x, y = col * TILE_SIZE, row * TILE_SIZE
    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 3)

    if reveal or revealed[row][col]:
        text = FONT.render(grid[row][col], True, BLACK)
        screen.blit(text, (x + TILE_SIZE // 3, y + TILE_SIZE // 4))


# Vérifie si toutes les paires sont trouvées
def all_found():
    return all(all(row) for row in revealed)


# Boucle principale
def main():
    show_initial_grid()
    screen.fill(WHITE)

    first_choice = None
    running = True
    while running:
        screen.fill(WHITE)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                draw_tile(row, col)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE

                if not revealed[row][col]:
                    revealed[row][col] = True
                    if first_choice is None:
                        first_choice = (row, col)
                    else:
                        r1, c1 = first_choice
                        if grid[r1][c1] != grid[row][col]:
                            pygame.display.flip()
                            pygame.time.delay(500)
                            revealed[r1][c1] = False
                            revealed[row][col] = False
                        first_choice = None

        if all_found():
            screen.fill(WHITE)
            text = FONT.render("Bravo, mini-jeu suivant débloqué !", True, BLACK)
            screen.blit(text, (WIDTH // 30, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
