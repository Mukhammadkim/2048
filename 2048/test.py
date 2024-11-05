import random
import pygame
import sys

pygame.init()

WINDOW_SIZE = 400
GRID_SIZE = 4
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

BACKGROUND_COLOR = (187, 173, 160)
CELL_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TEXT_COLOR = (119, 110, 101)
EMPTY_CELL_COLOR = (205, 193, 180)

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("2048")

font = pygame.font.Font(None, 50)

def initialize_game():
    """Инициализация начальной сетки."""
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid

def add_new_tile(grid):
    """Добавление нового числа (2 или 4) в случайную пустую ячейку."""
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = random.choice([2, 4])

def draw_grid(grid):
    """Отображение сетки на экране."""
    screen.fill(BACKGROUND_COLOR)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = grid[r][c]
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            pygame.draw.rect(screen, CELL_COLORS.get(value, EMPTY_CELL_COLOR), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
            if value != 0:
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    pygame.display.update()

def compress(grid):
    """Сдвиг всех чисел в сетке влево (передвижение пустых ячеек)."""
    new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        pos = 0
        for c in range(GRID_SIZE):
            if grid[r][c] != 0:
                new_grid[r][pos] = grid[r][c]
                pos += 1
    return new_grid

def merge(grid):
    """Объединение одинаковых чисел, если они находятся рядом."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r][c + 1] and grid[r][c] != 0:
                grid[r][c] *= 2
                grid[r][c + 1] = 0
    return grid

def reverse(grid):
    """Переворачиваем строку (для движения вправо)."""
    return [row[::-1] for row in grid]

def transpose(grid):
    """Транспонируем сетку (для движения вверх и вниз)."""
    return [list(row) for row in zip(*grid)]

def move_left(grid):
    """Двигаем все числа влево, сливаем одинаковые."""
    grid = compress(grid)
    grid = merge(grid)
    grid = compress(grid)
    return grid

def move_right(grid):
    """Двигаем все числа вправо."""
    grid = reverse(grid)
    grid = move_left(grid)
    grid = reverse(grid)
    return grid

def move_up(grid):
    """Двигаем все числа вверх."""
    grid = transpose(grid)
    grid = move_left(grid)
    grid = transpose(grid)
    return grid

def move_down(grid):
    """Двигаем все числа вниз."""
    grid = transpose(grid)
    grid = move_right(grid)
    grid = transpose(grid)
    return grid

def check_game_over(grid):
    """Проверяем, можно ли продолжить игру (есть ли ходы)."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                return False
            if c < GRID_SIZE - 1 and grid[r][c] == grid[r][c + 1]:
                return False
            if r < GRID_SIZE - 1 and grid[r][c] == grid[r + 1][c]:
                return False
    return True

def main():
    grid = initialize_game()
    clock = pygame.time.Clock()

    while True:
        draw_grid(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    grid = move_left(grid)
                    add_new_tile(grid)
                elif event.key == pygame.K_RIGHT:
                    grid = move_right(grid)
                    add_new_tile(grid)
                elif event.key == pygame.K_UP:
                    grid = move_up(grid)
                    add_new_tile(grid)
                elif event.key == pygame.K_DOWN:
                    grid = move_down(grid)
                    add_new_tile(grid)

        if check_game_over(grid):
            pygame.display.set_caption("2048 - Game Over!")
            break

        clock.tick(10)

if __name__ == "__main__":
    main()
