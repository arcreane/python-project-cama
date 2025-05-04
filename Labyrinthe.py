import pygame

pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labyrinthe Pygame")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 100)
RED = (255, 0, 0)

# Grille du labyrinthe : 0 = vide, 1 = mur, 2 = arrivée
maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,0,1],
    [1,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,1,1],
    [1,0,0,1,0,1,0,1,0,1],
    [1,1,1,1,0,1,0,1,0,1],
    [1,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,2,1],
    [1,1,1,1,1,1,1,1,1,1],
]

# Constantes
TILE_SIZE = WIDTH // len(maze[0])

# Joueur
player_pos = [1, 1]

# Boucle principale
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    # Affichage du labyrinthe
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            tile = maze[row][col]
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            if tile == 1:
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE))
            elif tile == 2:
                pygame.draw.rect(screen, GREEN, (x, y, TILE_SIZE, TILE_SIZE))

    # Affichage du joueur
    pygame.draw.rect(screen, BLUE, (player_pos[1]*TILE_SIZE+5, player_pos[0]*TILE_SIZE+5, TILE_SIZE-10, TILE_SIZE-10))

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Contrôles clavier
    keys = pygame.key.get_pressed()
    move = [0, 0]
    if keys[pygame.K_UP]:
        move = [-1, 0]
    elif keys[pygame.K_DOWN]:
        move = [1, 0]
    elif keys[pygame.K_LEFT]:
        move = [0, -1]
    elif keys[pygame.K_RIGHT]:
        move = [0, 1]

    new_pos = [player_pos[0] + move[0], player_pos[1] + move[1]]

    # Collision avec les murs
    if maze[new_pos[0]][new_pos[1]] != 1:
        player_pos = new_pos



    # Arrivée
    if maze[player_pos[0]][player_pos[1]] == 2:
        font = pygame.font.SysFont(None, 60)
        text = font.render("Gagné ! 🎉", True, RED)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(10)

pygame.quit()

