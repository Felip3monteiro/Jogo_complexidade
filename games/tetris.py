import pygame
import random

pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Tetris")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

colors = [BLACK, RED, GREEN, BLUE]

# Configurações de grid
grid_width, grid_height = 10, 20
block_size = 30

# Peças do Tetris
pieces = [
    [[1, 1, 1], [0, 1, 0]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]]
]

# Classe Tetris
class Tetris:
    def __init__(self):
        self.score = 0
        self.board = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        self.new_piece()

    def new_piece(self):
        self.piece = random.choice(pieces)
        self.piece_x = grid_width // 2 - len(self.piece[0]) // 2
        self.piece_y = 0

    def rotate(self):
        self.piece = [list(row) for row in zip(*self.piece[::-1])]

    def valid_position(self, offset_x=0, offset_y=0):
        for y, row in enumerate(self.piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.piece_x + x + offset_x
                    new_y = self.piece_y + y + offset_y
                    if new_x < 0 or new_x >= grid_width or new_y >= grid_height or (new_y >= 0 and self.board[new_y][new_x]):
                        return False
        return True

    def place_piece(self):
        for y, row in enumerate(self.piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.piece_y + y][self.piece_x + x] = cell
        self.clear_lines()
        self.new_piece()
        if not self.valid_position():
            self.game_over()

    def clear_lines(self):
        lines_to_clear = [y for y, row in enumerate(self.board) if all(row)]
        for y in lines_to_clear:
            self.board.pop(y)
            self.board.insert(0, [0 for _ in range(grid_width)])
            self.score += 100

    def game_over(self):
        self.__init__()

    def draw(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                pygame.draw.rect(screen, colors[cell], (x * block_size, y * block_size, block_size, block_size))
        for y, row in enumerate(self.piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, colors[cell], ((self.piece_x + x) * block_size, (self.piece_y + y) * block_size, block_size, block_size))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(text, (10, 10))

# Função principal do jogo
def main():
    clock = pygame.time.Clock()
    tetris = Tetris()
    fall_time = 0

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.piece_x -= 1
                    if not tetris.valid_position():
                        tetris.piece_x += 1
                if event.key == pygame.K_RIGHT:
                    tetris.piece_x += 1
                    if not tetris.valid_position():
                        tetris.piece_x -= 1
                if event.key == pygame.K_DOWN:
                    tetris.piece_y += 1
                    if not tetris.valid_position():
                        tetris.piece_y -= 1
                        tetris.place_piece()
                if event.key == pygame.K_UP:
                    tetris.rotate()
                    if not tetris.valid_position():
                        tetris.rotate()
                        tetris.rotate()
                        tetris.rotate()

        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time > 500:
            fall_time = 0
            tetris.piece_y += 1
            if not tetris.valid_position():
                tetris.piece_y -= 1
                tetris.place_piece()

        tetris.draw()
        pygame.display.flip()

main()
