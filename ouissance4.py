import pygame
import sys
import numpy as np
import random

# Paramètres du jeu
LARGEUR, HAUTEUR = 700, 600
TAILLE_CASE = 100
RAYON_JETON = TAILLE_CASE // 2 - 5
COLONNES, LIGNES = 7, 6
BLEU, BLANC, ROUGE, JAUNE = (0, 0, 255), (255, 255, 255), (255, 0, 0), (255, 255, 0)

# Initialisation de Pygame
pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Puissance 4 - VS Ordinateur")


def creer_grille():
    return np.zeros((LIGNES, COLONNES), dtype=int)


def afficher_grille(grille):
    fenetre.fill(BLEU)
    for c in range(COLONNES):
        for l in range(LIGNES):
            pygame.draw.rect(fenetre, BLANC, (c * TAILLE_CASE, l * TAILLE_CASE + TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
            pygame.draw.circle(fenetre, (0, 0, 0),
                               (c * TAILLE_CASE + TAILLE_CASE // 2, l * TAILLE_CASE + TAILLE_CASE + TAILLE_CASE // 2),
                               RAYON_JETON)

    for c in range(COLONNES):
        for l in range(LIGNES):
            if grille[l][c] == 1:
                pygame.draw.circle(fenetre, ROUGE,
                                   (c * TAILLE_CASE + TAILLE_CASE // 2, (l + 1) * TAILLE_CASE + TAILLE_CASE // 2),
                                   RAYON_JETON)
            elif grille[l][c] == 2:
                pygame.draw.circle(fenetre, JAUNE,
                                   (c * TAILLE_CASE + TAILLE_CASE // 2, (l + 1) * TAILLE_CASE + TAILLE_CASE // 2),
                                   RAYON_JETON)
    pygame.display.update()


def colonne_disponible(grille, colonne):
    return grille[0][colonne] == 0


def placer_jeton(grille, colonne, joueur):
    for l in range(LIGNES - 1, -1, -1):
        if grille[l][colonne] == 0:
            grille[l][colonne] = joueur
            return


def verif_victoire(grille, joueur):
    # Vérification horizontale
    for l in range(LIGNES):
        for c in range(COLONNES - 3):
            if all(grille[l][c + i] == joueur for i in range(4)):
                return True

    # Vérification verticale
    for c in range(COLONNES):
        for l in range(LIGNES - 3):
            if all(grille[l + i][c] == joueur for i in range(4)):
                return True

    # Vérification diagonale /
    for l in range(3, LIGNES):
        for c in range(COLONNES - 3):
            if all(grille[l - i][c + i] == joueur for i in range(4)):
                return True

    # Vérification diagonale \
    for l in range(LIGNES - 3):
        for c in range(COLONNES - 3):
            if all(grille[l + i][c + i] == joueur for i in range(4)):
                return True

    return False


def choisir_colonne_ordi(grille):
    colonnes_valides = [c for c in range(COLONNES) if colonne_disponible(grille, c)]
    return random.choice(colonnes_valides) if colonnes_valides else None


def jeu():
    grille = creer_grille()
    game_over = False
    tour = 0
    afficher_grille(grille)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if tour % 2 == 0:
            # Tour du joueur (humain)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0]
                    colonne = x // TAILLE_CASE

                    if colonne_disponible(grille, colonne):
                        placer_jeton(grille, colonne, 1)
                        afficher_grille(grille)

                        if verif_victoire(grille, 1):
                            print("Le joueur a gagné !")
                            game_over = True
                        tour += 1
        else:
            # Tour de l'ordinateur
            pygame.time.wait(500)  # Petite pause pour simuler la réflexion
            colonne = choisir_colonne_ordi(grille)

            if colonne is not None:
                placer_jeton(grille, colonne, 2)
                afficher_grille(grille)

                if verif_victoire(grille, 2):
                    print("L'ordinateur a gagné !")
                    game_over = True
                tour += 1

    pygame.time.wait(3000)
    pygame.quit()


jeu()
