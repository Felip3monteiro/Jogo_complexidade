import pygame, sys
from game import Game
from colors import Colors

pygame.init()  # inicializa o pygame

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()

# Função para ajustar a velocidade do jogo com base na pontuação
def adjust_speed(score):
    # Quanto maior a pontuação, mais rápido o jogo
    if score < 500:
        return 200  # intervalo de 200ms para pontuação abaixo de 500
    elif score < 1000:
        return 150  # intervalo de 150ms para pontuação entre 500 e 1000
    elif score < 1500:
        return 120  # intervalo de 120ms para pontuação entre 1000 e 1500
    else:
        return 100  # intervalo de 100ms para pontuação acima de 1500

# Inicializando o evento de atualização com o intervalo base
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, adjust_speed(game.score))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
            # Ajustando a velocidade do jogo com base na pontuação
            pygame.time.set_timer(GAME_UPDATE, adjust_speed(game.score))

    # Desenhando os elementos na tela
    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))

    if game.game_over == True:
        screen.blit(game_over_surface, (320, 450, 50, 50))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
        centery=score_rect.centery))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)
