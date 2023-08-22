import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
BLOCK_SIZE = 30
GRID_WIDTH = 12
WIDTH = GRID_WIDTH * BLOCK_SIZE
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Tamaño de los bloques y la cuadrícula
GRID_HEIGHT = HEIGHT // BLOCK_SIZE

# del board[row]  and countTimeIncrement
countDelBoardRow = 0
countTimeIncrement = 2 # velocity initial

# Clase para la pieza actual
class Piece:
    def __init__(self):
        self.x = GRID_WIDTH // 2
        self.y = 0
        self.shape = random.choice(tetrominoes)
        self.color = random.choice(colors)

    def draw(self):
        # Dibuja la pieza actual en la pantalla
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    pygame.draw.rect(
                        WIN,
                        self.color,
                        (
                            (self.x * BLOCK_SIZE) + (col * BLOCK_SIZE),
                            (self.y * BLOCK_SIZE) + (row * BLOCK_SIZE),
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )

    def move_down(self):
        # Mueve la pieza hacia abajo si no hay colisión
        if not self.collide(self.x, self.y + 1, self.shape):
            self.y += 1
        else:
            self.freeze()

    def move_left(self):
        # Mueve la pieza hacia la izquierda si no hay colisión
        if not self.collide(self.x - 1, self.y, self.shape):
            self.x -= 1

    def move_right(self):
        # Mueve la pieza hacia la derecha si no hay colisión
        if not self.collide(self.x + 1, self.y, self.shape):
            self.x += 1

    def rotate(self):
        # Rota la pieza en sentido horario si no hay colisión
        new_shape = list(zip(*reversed(self.shape)))
        if not self.collide(self.x, self.y, new_shape):
            self.shape = new_shape

    def freeze(self):
        # Congela la pieza actual en el tablero
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    board[self.y + row][self.x + col] = self.color
        self.__init__()
        remove_completed_rows(board)

    def collide(self, x, y, shape):
        # Comprueba si hay colisión entre la pieza y el tablero
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if (
                    shape[row][col]
                    and (
                        y + row >= GRID_HEIGHT
                        or x + col < 0
                        or x + col >= GRID_WIDTH
                        or board[y + row][x + col]
                    )
                ):
                    return True
        return False

def remove_completed_rows(board):
    global countDelBoardRow
    global countTimeIncrement
    rows_to_remove = []
    for row in range(GRID_HEIGHT):
        if all(board[row]):
            rows_to_remove.append(row)

    for row in rows_to_remove:
        countDelBoardRow += 1
        if countDelBoardRow % 5 == 0:
            countTimeIncrement +=1
            print(f'velocity game is {countTimeIncrement}')
        del board[row]
        board.insert(0, [0] * GRID_WIDTH)

    return len(rows_to_remove)

# Lista de tetrominos y colores

# Piezas: I-Tetromino: [[1, 1, 1, 1]] (línea larga) ||  O-Tetromino:[[1, 1], [1, 1]] (cuadrado)
tetrominoes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
]
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 165, 0),
]

# Tablero del juego
board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Variables del juego
running = True
clock = pygame.time.Clock()
piece = Piece()
show_start_screen = True
game_over = False

def game_over_screen():
    global countTimeIncrement
    WIN.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text, text_rect)
    restart_text = font.render("Pulse R para volver a jugar", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    WIN.blit(restart_text, restart_rect)
    countTimeIncrement = 3
    pygame.display.update()

# Bucle principal del juego
while running:
    clock.tick(countTimeIncrement)  # Controla la velocidad de caída de las piezas

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if show_start_screen and event.key == pygame.K_RETURN:
                show_start_screen = False
            elif event.key == pygame.K_LEFT:
                piece.move_left()
            elif event.key == pygame.K_RIGHT:
                piece.move_right()
            elif event.key == pygame.K_DOWN:
                piece.move_down()
            elif event.key == pygame.K_UP:
                piece.rotate()
            elif game_over and event.key == pygame.K_r:
                # Volver a jugar
                game_over = False
                piece = Piece()
                board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    if not game_over and not show_start_screen:
        piece.move_down()
        if piece.collide(piece.x, piece.y, piece.shape):
            game_over = True

    WIN.fill(BLACK)

    if show_start_screen:
        # Mostrar la pantalla de inicio
        font = pygame.font.Font(None, 36)
        text = font.render("Pulse Enter para empezar", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WIN.blit(text, text_rect)
    elif game_over:
        # Mostrar la pantalla de Game Over
        game_over_screen()
    else:
        # Dibujar el tablero y la pieza actual
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                pygame.draw.rect(
                    WIN,
                    board[row][col],
                    (
                        col * BLOCK_SIZE,
                        row * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    ),
                )

        piece.draw()

    pygame.display.update()

pygame.quit()
