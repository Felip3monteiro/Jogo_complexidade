import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jogo de Nave Inspirado no Atari")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# FPS e Relógio
FPS = 60
clock = pygame.time.Clock()

# Configurações da nave
ship_width, ship_height = 50, 40
ship = pygame.Rect(width // 2 - ship_width // 2, height - ship_height - 10, ship_width, ship_height)
ship_speed = 10

# Configurações dos tiros
bullet_width, bullet_height = 5, 10
bullets = []
bullet_speed = 7

# Configurações dos inimigos
enemy_width, enemy_height = 50, 40
enemies = []
enemy_speed = 5

# Taxa de geração de inimigos (quanto menor, mais rápido)
spawn_rate = 50

# Função para desenhar na tela
def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, ship)
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)
    for enemy in enemies:
        pygame.draw.rect(screen, WHITE, enemy)
    pygame.display.flip()

# Função para gerar inimigos
def spawn_enemy():
    x = random.randint(0, width - enemy_width)
    y = random.randint(-100, -40)
    enemy = pygame.Rect(x, y, enemy_width, enemy_height)
    enemies.append(enemy)

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(ship.centerx - bullet_width // 2, ship.top, bullet_width, bullet_height)
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship.left > 0:
        ship.move_ip(-ship_speed, 0)
    if keys[pygame.K_RIGHT] and ship.right < width:
        ship.move_ip(ship_speed, 0)

    for bullet in bullets[:]:
        bullet.move_ip(0, -bullet_speed)
        if bullet.bottom < 0:
            bullets.remove(bullet)

    for enemy in enemies[:]:
        enemy.move_ip(0, enemy_speed)
        if enemy.top > height:
            enemies.remove(enemy)
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Geração de inimigos com base na taxa de spawn (spawn_rate)
    if random.randint(1, spawn_rate) == 1:
        spawn_enemy()

    draw()
    clock.tick(FPS)
