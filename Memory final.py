import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)

# Chargement de la police
FONT = pygame.font.Font(pygame.font.match_font("segoeuisymbol", True), 50)

# Création de la grille
symbols = ["\u2605", "\u2600", "\u2601", "\u2660", "\u2666", "\u2764", "\u266B", "\u273F"]
symbols = symbols[:GRID_SIZE * GRID_SIZE // 2] * 2
random.shuffle(symbols)
grid = [symbols[i * GRID_SIZE:(i + 1) * GRID_SIZE] for i in range(GRID_SIZE)]
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

# Fonction pour dessiner une case
def draw_tile(screen, row, col, reveal=False):
    x, y = col * TILE_SIZE, row * TILE_SIZE
    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 3)
    if reveal or revealed[row][col]:
        text = FONT.render(grid[row][col], True, BLACK)
        screen.blit(text, (x + TILE_SIZE // 3, y + TILE_SIZE // 4))

# Fonction principale
def main():
    global revealed
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu de mémoire")

    # Affiche toutes les cases pendant 3 secondes
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            draw_tile(screen, row, col, reveal=True)
    pygame.display.flip()
    time.sleep(5)

    first_choice = None
    running = True
    while running:
        screen.fill(WHITE)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                draw_tile(screen, row, col)
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

        if all(all(row) for row in revealed):
            screen.fill(WHITE)
            text = FONT.render("Bravo !", True, BLACK)
            screen.blit(text, (WIDTH // 3, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)

            # Lance le mini-jeu suivant avec une grille plus grande
            start_next_level(GRID_SIZE + 2)
            return  # Quitte cette instance de main()

    pygame.quit()

# Fonction pour lancer une nouvelle partie avec une grille plus grande
def start_next_level(new_grid_size):
    global GRID_SIZE, TILE_SIZE, symbols, grid, revealed

    GRID_SIZE = new_grid_size
    TILE_SIZE = WIDTH // GRID_SIZE

    # Génère les symboles nécessaires pour la nouvelle taille
    unique_symbols_needed = (GRID_SIZE * GRID_SIZE) // 2
    base_symbols = ["\u2605", "\u2600", "\u2601", "\u2660", "\u2666", "\u2764", "\u266B", "\u273F",
                    "\u25B2", "\u25A0", "\u25C6", "\u25CF", "\u25E3", "\u2602", "\u2618", "\u2620",
                    "\u262F", "\u263A", "\u263C", "\u260E", "\u2663", "\u2721"]
    selected_symbols = base_symbols[:unique_symbols_needed] * 2
    random.shuffle(selected_symbols)

    # Nouvelle grille et cases révélées
    grid = [selected_symbols[i * GRID_SIZE:(i + 1) * GRID_SIZE] for i in range(GRID_SIZE)]
    revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Relance le jeu avec la nouvelle taille
    main()

# Point d’entrée du programme
if __name__ == "__main__":
    main()
