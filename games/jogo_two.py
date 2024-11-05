import pygame
import random
import sys
import time

# Inicializa o Pygame
pygame.init()

# Configurações da tela em modo fullscreen
largura, altura = 400, 600
tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
pygame.display.set_caption("Flappy Bird")

# Defina algumas cores
AZUL_CLARO = (135, 206, 235)
VERDE = (34, 139, 34)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Configurações do pássaro
bird_x = 100
bird_y = altura // 2
bird_largura = 30
bird_altura = 30
bird_velocidade = 0
gravidade = 0.5
pulo = -10

# Configurações dos tubos
tubo_largura = 80
tubo_velocidade = 5
distancia_entre_tubos = 200
espaco_entre_tubos_iniciais = 300  # Distância entre os três primeiros tubos
tubos = []

# Função para criar um tubo em uma posição x específica
def criar_tubo(x_pos):
    altura_topo = random.randint(100, 400)
    tubos.append((x_pos, altura_topo))

# Adiciona os três primeiros pares de tubos fora da tela
for i in range(3):
    criar_tubo(largura + i * espaco_entre_tubos_iniciais)

# Controle de frames por segundo
clock = pygame.time.Clock()

# Variável de pontuação
pontuacao = 0
fonte = pygame.font.SysFont(None, 40)

# Variável de estado do jogo
jogo_ativo = False

# Função para mostrar o botão "Jogar"
def mostrar_botao_jogar():
    botao_rect = pygame.Rect(largura // 2 - 50, altura // 2 - 25, 100, 50)
    pygame.draw.rect(tela, BRANCO, botao_rect)
    texto_jogar = fonte.render("Jogar", True, PRETO)
    tela.blit(texto_jogar, (botao_rect.x + 20, botao_rect.y + 10))
    return botao_rect

# Função de contagem regressiva
def contagem_regressiva():
    for i in range(3, 0, -1):
        tela.fill(AZUL_CLARO)
        texto_contagem = fonte.render(str(i), True, PRETO)
        tela.blit(texto_contagem, (largura // 2 - 10, altura // 2 - 20))
        pygame.display.flip()
        time.sleep(1)

# Loop principal do jogo
while True:
    # Lida com eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()  # Sai do jogo ao pressionar ESC
            elif evento.key == pygame.K_SPACE and jogo_ativo:
                bird_velocidade = pulo  # Faz o pássaro pular
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if not jogo_ativo:
                if botao_rect.collidepoint(evento.pos):
                    contagem_regressiva()  # Faz a contagem regressiva
                    jogo_ativo = True  # Inicia o jogo

    # Desenha a tela inicial e o botão "Jogar" quando o jogo não está ativo
    if not jogo_ativo:
        tela.fill(AZUL_CLARO)
        botao_rect = mostrar_botao_jogar()
        pygame.display.flip()
        continue

    # Movimento do pássaro
    bird_velocidade += gravidade
    bird_y += bird_velocidade

    # Movimento dos tubos
    for i in range(len(tubos)):
        tubos[i] = (tubos[i][0] - tubo_velocidade, tubos[i][1])

    # Remove tubos fora da tela e cria novos
    if tubos[0][0] < -tubo_largura:
        tubos.pop(0)
        criar_tubo(tubos[-1][0] + espaco_entre_tubos_iniciais)  # Cria um novo tubo após o último

        pontuacao += 1  # Aumenta a pontuação ao passar por um par de tubos

    # Verifica colisão
    for tubo_x, altura_topo in tubos:
        if (bird_x + bird_largura > tubo_x and bird_x < tubo_x + tubo_largura):
            if bird_y < altura_topo or bird_y + bird_altura > altura_topo + distancia_entre_tubos:
                pygame.quit()
                sys.exit()

    # Verifica se o pássaro toca o chão ou o topo
    if bird_y < 0 or bird_y > altura:
        pygame.quit()
        sys.exit()

    # Limpa a tela
    tela.fill(AZUL_CLARO)

    # Desenha o pássaro
    pygame.draw.rect(tela, AMARELO, (bird_x, bird_y, bird_largura, bird_altura))

    # Desenha os tubos
    for tubo_x, altura_topo in tubos:
        pygame.draw.rect(tela, VERDE, (tubo_x, 0, tubo_largura, altura_topo))
        pygame.draw.rect(tela, VERDE, (tubo_x, altura_topo + distancia_entre_tubos, tubo_largura, altura))

    # Desenha a pontuação
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, (0, 0, 0))
    tela.blit(texto_pontuacao, (10, 10))

    # Atualiza a tela
    pygame.display.flip()

    # Limita o loop para rodar a 60 vezes por segundo
    clock.tick(60)
