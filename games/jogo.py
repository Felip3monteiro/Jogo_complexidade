import pygame
import random

pygame.init()
tela = pygame.display.set_mode((1280, 720))
frame = pygame.time.Clock()
looping = True
dt = 0

# Configurações das árvores
num_arvores = 20
cor_arvores = (34, 139, 34)
arvore_largura = 20
arvore_altura = 50
distancia_minima_arvores = 150

# Configurações do jogador
player_pos = pygame.Vector2(640, 360)
inventario = []
madeira_por_coleta = 1

# Configurações dos bots
num_bots = 5
cor_bot = (0, 0, 255)
bot_raio = 20
bots = []
direcoes_bots = []

# Define os limites do "mundo"
world_limit_left = 0
world_limit_right = tela.get_width() * 2
world_limit_top = 0
world_limit_bottom = tela.get_height() * 2

for _ in range(num_bots):
    x = random.randint(world_limit_left, world_limit_right - arvore_largura)
    y = random.randint(world_limit_top, world_limit_bottom - arvore_altura)
    bots.append(pygame.Vector2(x, y))
    direcoes_bots.append(pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])))

# Gera posições para as árvores com espaçamento mínimo
posicoes_arvores = []
while len(posicoes_arvores) < num_arvores:
    x = random.randint(world_limit_left, world_limit_right - arvore_largura)
    y = random.randint(world_limit_top + tela.get_height() // 2, world_limit_bottom - arvore_altura)
    if all((pygame.Vector2(x, y).distance_to(pygame.Vector2(px, py)) > distancia_minima_arvores)
           for px, py in posicoes_arvores):
        posicoes_arvores.append((x, y))

# Lista para armazenar paredes construídas
paredes = []

def verifica_colisao(player_pos, posicoes_arvores):
    for pos in posicoes_arvores:
        x, y = pos
        if (player_pos.x + 40 > x and player_pos.x - 40 < x + arvore_largura and
            player_pos.y + 40 > y and player_pos.y - 40 < y + arvore_altura):
            return pos
    return None

def verifica_colisao_paredes(player_pos, paredes):
    for parede in paredes:
        x, y, largura, altura = parede
        if (player_pos.x + 40 > x and player_pos.x - 40 < x + largura and
            player_pos.y + 40 > y and player_pos.y - 40 < y + altura):
            return True
    return False

def verifica_colisao_bots(player_pos, bots):
    for bot in bots:
        if player_pos.distance_to(bot) < 40 + bot_raio:
            return True
    return False

while looping:
    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            looping = False

    tela.fill("white")
    
    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    movimento = pygame.Vector2(0, 0)
    if keys[pygame.K_w]:
        movimento.y -= 300 * dt
    if keys[pygame.K_s]:
        movimento.y += 300 * dt
    if keys[pygame.K_a]:
        movimento.x -= 300 * dt
    if keys[pygame.K_d]:
        movimento.x += 300 * dt

    # Aplica o movimento do jogador e verifica as colisões e os limites
    nova_posicao_jogador = player_pos + movimento
    if (world_limit_left < nova_posicao_jogador.x < world_limit_right - 40 and
        world_limit_top < nova_posicao_jogador.y < world_limit_bottom - 40 and
        not verifica_colisao(nova_posicao_jogador, posicoes_arvores) and
        not verifica_colisao_bots(nova_posicao_jogador, bots) and
        not verifica_colisao_paredes(nova_posicao_jogador, paredes)):
        player_pos = nova_posicao_jogador

    # Atualização dos bots
    for i, bot in enumerate(bots):
        nova_posicao_bot = bot + direcoes_bots[i] * 100 * dt
        # Verifica se o bot está dentro dos limites do mundo
        if world_limit_left < nova_posicao_bot.x < world_limit_right - bot_raio:
            bot.x = nova_posicao_bot.x
        else:
            direcoes_bots[i].x *= -1  # Inverte a direção ao colidir com a borda
        
        if world_limit_top < nova_posicao_bot.y < world_limit_bottom - bot_raio:
            bot.y = nova_posicao_bot.y
        else:
            direcoes_bots[i].y *= -1  # Inverte a direção ao colidir com a borda

    # Calcula o offset para centralizar a câmera no jogador
    offset_x = tela.get_width() // 2 - player_pos.x
    offset_y = tela.get_height() // 2 - player_pos.y

    # Desenha as áreas pretas ao redor da área de jogo
    pygame.draw.rect(tela, "black", (0, 0, tela.get_width(), offset_y))  # Parte superior
    pygame.draw.rect(tela, "white", (0, tela.get_height() + offset_y, tela.get_width(), tela.get_height() - offset_y))  # Parte inferior
    pygame.draw.rect(tela, "black", (0, 0, offset_x, tela.get_height()))  # Parte esquerda
    pygame.draw.rect(tela, "black", (tela.get_width() + offset_x, 0, tela.get_width() - offset_x, tela.get_height()))  # Parte direita

    # Desenha o jogador
    pygame.draw.circle(tela, "red", (tela.get_width() // 2, tela.get_height() // 2), 40)

    # Desenha as árvores usando as posições com o offset da câmera
    for pos in posicoes_arvores:
        x, y = pos
        pygame.draw.rect(tela, cor_arvores, (x + offset_x, y + offset_y, arvore_largura, arvore_altura))
        pygame.draw.circle(tela, (139, 69, 19), (x + arvore_largura // 2 + offset_x, y + offset_y), 25)

    # Desenha os bots
    for bot in bots:
        pygame.draw.circle(tela, cor_bot, (bot.x + offset_x, bot.y + offset_y), bot_raio)

    # Exibe o inventário na tela
    font = pygame.font.Font(None, 36)
    inventario_texto = f"Inventário: {sum(inventario)} madeira"
    texto_surface = font.render(inventario_texto, True, "black")
    tela.blit(texto_surface, (10, 10))

    # Construção de paredes
    if keys[pygame.K_e] and sum(inventario) > 0:
        pos_x = player_pos.x
        pos_y = player_pos.y
        paredes.append((pos_x - 20, pos_y - 20, 40, 40))
        inventario.pop()

    # Desenha as paredes construídas
    for parede in paredes:
        x, y, largura, altura = parede
        pygame.draw.rect(tela, (139, 69, 19), (x + offset_x, y + offset_y, largura, altura))

    pygame.display.flip()
    dt = frame.tick(60) / 1000

pygame.quit()
