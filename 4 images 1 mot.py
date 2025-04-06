import pygame
import os


pygame.init()

# Fenêtre
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4 Images 1 Mot")
font = pygame.font.SysFont("arial", 32)
clock = pygame.time.Clock()



# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
RED = (215, 0, 0)
TRANSPARENT= (0, 0 , 0, 0)

niveau = 1
solution = ""
images = []
input_text = ""
# Compte combien de dossiers 'niveauX' existent
max_niveaux = len([d for d in os.listdir() if d.startswith("niveau") and os.path.isdir(d)])
print(f"[DEBUG] Niveaux détectés : {max_niveaux}")

def charger_niveau(n):
    global images, solution
    images.clear()

    dossier = f"niveau{n}"
    if not os.path.exists(dossier):
        return False

    try:
        for i in range(1, 5):
            path = os.path.join(dossier, f"{i}.png")
            if not os.path.exists(path):
                print(f"[ERROR] L'image {path} est manquante.")
                return False
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (180, 180))
            images.append(image)

        with open(os.path.join(dossier, "mot.txt"), "r", encoding="utf-8") as f:
            solution = f.read().strip().lower()

        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

# Modification de la condition de fin de jeu
if niveau > max_niveaux:
    msg = font.render("Jeu terminé, vous avez gagné !", True, BLACK)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Attendre 2 secondes avant de quitter
    running = False

def afficher_images():
    for i in range(4):
        x = 150 + (i % 2) * 200
        y = 80 + (i // 2) * 200
        screen.blit(images[i], (x, y))

def afficher_texte():
    # Boîte d'entrée
    pygame.draw.rect(screen, TRANSPARENT, (190, 480, 300, 40), )
    pygame.draw.rect(screen, WHITE, (190, 480, 300, 40), 3)
    texte = font.render(input_text.upper(),  False, WHITE)
    screen.blit(texte, (260, 475))

    # Label
    niveau_txt = font.render(f"Niveau {niveau}", True, RED, )
    screen.blit(niveau_txt, (10, 10))

def afficher_message(message, color):
    msg = font.render(message, True, color)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 530))

# Lancement
en_cours = charger_niveau(niveau)
message = "1"
message_timer = 0

running = True
while running:
    screen.fill(BLACK)
    if not en_cours:
        msg = font.render(" Jeu terminé !", False, WHITE )
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        continue

    afficher_images()
    afficher_texte()

    if message and pygame.time.get_ticks() - message_timer < 2000:
        afficher_message(message, BLUE if message.startswith("Bravo") else (255, 0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if input_text.lower() == solution:
                    message = "Bravo ! Niveau suivant 🚀"
                    niveau += 1
                    en_cours = charger_niveau(niveau)
                    input_text = ""
                    message_timer = pygame.time.get_ticks()
                else:
                    message = "Mauvaise réponse ❌"
                    message_timer = pygame.time.get_ticks()
            elif event.unicode.isalpha():
                input_text += event.unicode

    clock.tick(30)

pygame.quit()