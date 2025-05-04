import pygame
import sys
import random
import time
import os
import numpy as np

# === CONSTANTES === #
WIDTH, HEIGHT = 700, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
RED = (215, 0, 0)
YELLOW = (255, 222, 33)
GRAY = (200, 200, 200)

# === INITIALISATION === #
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Jeux")
font = pygame.font.SysFont("arial", 32)
clock = pygame.time.Clock()

# === MENU PRINCIPAL === #
def menu_principal():
    while True:
        screen.fill(BLACK)
        titre = font.render("Choisis un jeu :", True, WHITE)
        options = [
            "1 - Jeu de Mémoire",
            "2 - Puissance 4",
            "3 - 4 Images 1 Mot",
            "ESC - Quitter"
        ]
        screen.blit(titre, (WIDTH // 2 - titre.get_width() // 2, 100))
        for i, opt in enumerate(options):
            texte = font.render(opt, True, BLUE)
            screen.blit(texte, (WIDTH // 2 - texte.get_width() // 2, 180 + i * 60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    jeu_memoire()
                elif event.key == pygame.K_2:
                    jeu_puissance4()
                elif event.key == pygame.K_3:
                    jeu_4images_un_mot()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

# === JEU 1 : MEMOIRE === #
# Paramètres dynamiques
GRID_SIZE = 4
TILE_SIZE = 100
WIDTH = GRID_SIZE * TILE_SIZE
HEIGHT = GRID_SIZE * TILE_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)



# Création initiale de la police (sera redimensionnée)
def get_font(tile_size):
    return pygame.font.Font(pygame.font.match_font("segoeuisymbol", True), tile_size // 2)

FONT = get_font(TILE_SIZE)

# Fonction pour dessiner une case
def draw_tile(screen, row, col, reveal=False):
    x, y = col * TILE_SIZE, row * TILE_SIZE
    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 3)
    if reveal or revealed[row][col]:
        text = FONT.render(grid[row][col], True, BLACK)
        screen.blit(text, (x + TILE_SIZE // 4, y + TILE_SIZE // 6))

# Fonction principale
def jeu_memoire():
    global revealed, WIDTH, HEIGHT, TILE_SIZE, FONT

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu de mémoire")

    # Affiche toutes les cases pendant 3 secondes
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            draw_tile(screen, row, col, reveal=True)
    pygame.display.flip()
    time.sleep(3)

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
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
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
            win_text = FONT.render("Bravo !", True, BLACK)
            screen.blit(win_text, (WIDTH // 3, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            start_next_level(GRID_SIZE + 2)
            return  # Redémarre avec nouvelle grille

# Nouvelle grille avec plus de cases
def start_next_level(new_grid_size):
    global GRID_SIZE, TILE_SIZE, WIDTH, HEIGHT, FONT, grid, revealed

    GRID_SIZE = new_grid_size
    TILE_SIZE = 100  # Garder taille constante
    WIDTH = GRID_SIZE * TILE_SIZE
    HEIGHT = GRID_SIZE * TILE_SIZE
    FONT = get_font(TILE_SIZE)

    pygame.display.set_mode((WIDTH, HEIGHT))

    base_symbols = ["\u2605", "\u2600", "\u2601", "\u2660", "\u2666", "\u2764", "\u266B", "\u273F",
                    "\u25B2", "\u25A0", "\u25C6", "\u25CF", "\u25E3", "\u2602", "\u2618", "\u2620",
                    "\u262F", "\u263A", "\u263C", "\u260E", "\u2663", "\u2721"]
    needed = (GRID_SIZE * GRID_SIZE) // 2
    symbols = (base_symbols[:needed] * 2)[:GRID_SIZE * GRID_SIZE]
    random.shuffle(symbols)
    grid = [symbols[i * GRID_SIZE:(i + 1) * GRID_SIZE] for i in range(GRID_SIZE)]
    revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

    jeu_memoire()

# Initialisation du premier niveau
base_symbols = ["\u2605", "\u2600", "\u2601", "\u2660", "\u2666", "\u2764", "\u266B", "\u273F"]
symbols = (base_symbols[:GRID_SIZE * GRID_SIZE // 2] * 2)
random.shuffle(symbols)
grid = [symbols[i * GRID_SIZE:(i + 1) * GRID_SIZE] for i in range(GRID_SIZE)]
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]


# === JEU 2 : PUISSANCE 4 === #
def jeu_puissance4():
    TAILLE_CASE = 100
    RAYON = TAILLE_CASE // 2 - 5
    COLONNES, LIGNES = 7, 6

    def creer_grille():
        return np.zeros((LIGNES, COLONNES), dtype=int)

    def afficher_grille(grille):
        screen.fill((0, 0, 255))
        for c in range(COLONNES):
            for l in range(LIGNES):
                pygame.draw.rect(screen, WHITE, (c * TAILLE_CASE, l * TAILLE_CASE + TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
                pygame.draw.circle(screen, BLACK, (c * TAILLE_CASE + TAILLE_CASE // 2, l * TAILLE_CASE + TAILLE_CASE + TAILLE_CASE // 2), RAYON)

        for c in range(COLONNES):
            for l in range(LIGNES):
                if grille[l][c] == 1:
                    pygame.draw.circle(screen, RED, (c * TAILLE_CASE + TAILLE_CASE // 2, (l + 1) * TAILLE_CASE + TAILLE_CASE // 2), RAYON)
                elif grille[l][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (c * TAILLE_CASE + TAILLE_CASE // 2, (l + 1) * TAILLE_CASE + TAILLE_CASE // 2), RAYON)
        pygame.display.update()

    def placer_jeton(grille, col, joueur):
        for l in range(LIGNES - 1, -1, -1):
            if grille[l][col] == 0:
                grille[l][col] = joueur
                return

    def verif_victoire(grille, j):
        for l in range(LIGNES):
            for c in range(COLONNES - 3):
                if all(grille[l][c + i] == j for i in range(4)):
                    return True
        for c in range(COLONNES):
            for l in range(LIGNES - 3):
                if all(grille[l + i][c] == j for i in range(4)):
                    return True
        for l in range(3, LIGNES):
            for c in range(COLONNES - 3):
                if all(grille[l - i][c + i] == j for i in range(4)):
                    return True
        for l in range(LIGNES - 3):
            for c in range(COLONNES - 3):
                if all(grille[l + i][c + i] == j for i in range(4)):
                    return True
        return False

    def choisir_colonne(grille):
        options = [c for c in range(COLONNES) if grille[0][c] == 0]
        return random.choice(options) if options else None

    grille = creer_grille()
    tour = 0
    game_over = False
    afficher_grille(grille)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if tour % 2 == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // TAILLE_CASE
                if grille[0][col] == 0:
                    placer_jeton(grille, col, 1)
                    if verif_victoire(grille, 1):
                        print("Le joueur a gagné !")
                        game_over = True
                    tour += 1
                    afficher_grille(grille)

        if tour % 2 == 1 and not game_over:
            pygame.time.wait(500)
            col = choisir_colonne(grille)
            if col is not None:
                placer_jeton(grille, col, 2)
                if verif_victoire(grille, 2):
                    print("L'ordinateur a gagné !")
                    game_over = True
                tour += 1
                afficher_grille(grille)

    pygame.time.wait(2000)

# === JEU 3 : 4 IMAGES 1 MOT === #
images = []
def jeu_4images_un_mot():
    niveau = 1
    input_text = ""
    essais = 0
    message = ""
    message_timer = 0


    def charger_niveau(n):
        global images, solution, indice
        images.clear()
        dossier = f"niveau{n}"
        if not os.path.exists(dossier):
            return False
        for i in range(1, 5):
            path = os.path.join(dossier, f"{i}.png")
            if not os.path.exists(path): return False
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (180, 180))
            images.append(img)
        with open(os.path.join(dossier, "mot.txt"), "r", encoding="utf-8") as f:
            solution = f.read().strip().lower()
        indice = solution[0].upper()
        return True

    def afficher_images():
        for i in range(4):
            x = 150 + (i % 2) * 200
            y = 80 + (i // 2) * 200
            screen.blit(images[i], (x, y))

    def afficher_texte():
        pygame.draw.rect(screen, GRAY, (190, 480, 300, 40), 0)
        pygame.draw.rect(screen, WHITE, (190, 480, 300, 40), 3)
        texte = font.render(input_text.upper(), False, BLACK)
        screen.blit(texte, (210, 483))
        niv = font.render(f"Niveau {niveau}", True, RED)
        screen.blit(niv, (10, 10))

    charger_niveau(niveau)
    running = True
    while running:
        screen.fill(BLACK)
        afficher_images()
        afficher_texte()
        if message and pygame.time.get_ticks() - message_timer < 2000:
            msg = font.render(message, True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 530))
        if essais >= 3 and not message.startswith("Bravo"):
            hint = font.render(f"Indice : {indice}", True, BLUE)
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 560))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_text.lower() == solution:
                        niveau += 1
                        input_text = ""
                        essais = 0
                        message = "Bravo !"
                        message_timer = pygame.time.get_ticks()
                        if not charger_niveau(niveau):
                            return
                    else:
                        essais += 1
                        message = "Mauvaise réponse"
                        message_timer = pygame.time.get_ticks()
                elif event.unicode.isalpha():
                    input_text += event.unicode
        clock.tick(30)

# === LANCEMENT === #
if __name__ == "__main__":
    menu_principal()