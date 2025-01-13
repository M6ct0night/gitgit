import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 480, 320
GRID_SIZE = 4
TILE_SIZE = 70
MARGIN = 10
GRID_TOP_OFFSET = (HEIGHT - (GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN)) // 2
GRID_LEFT_OFFSET = (WIDTH - (GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * MARGIN)) // 2
FONT_SIZE = 24
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLOR = {
    0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
    16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114),
    256: (237, 204, 97), 512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46)
}
TEXT_COLOR = (119, 110, 101)
SCORE_COLOR = (255, 255, 255)
TITLE_COLOR = (255, 255, 255)

# Pygame Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")
font = pygame.font.Font(None, FONT_SIZE)
title_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 28)

# Helper Functions
def draw_grid(grid, score):
    screen.fill(BACKGROUND_COLOR)

    # Draw Score
    score_text = score_font.render(f"Score: {score}", True, SCORE_COLOR)
    screen.blit(score_text, (20, 20))

    # Draw Tiles
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            rect = pygame.Rect(
                GRID_LEFT_OFFSET + col * (TILE_SIZE + MARGIN) + MARGIN,
                GRID_TOP_OFFSET + row * (TILE_SIZE + MARGIN) + MARGIN,
                TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(screen, TILE_COLOR.get(value, (60, 58, 50)), rect)
            if value > 0:
                text = font.render(str(value), True, TEXT_COLOR if value < 8 else SCORE_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def move(grid, direction):
    def merge(line):
        merged_line = [value for value in line if value != 0]
        for i in range(len(merged_line) - 1):
            if merged_line[i] == merged_line[i + 1]:
                merged_line[i] *= 2
                merged_line[i + 1] = 0
        merged_line = [value for value in merged_line if value != 0]
        return merged_line + [0] * (GRID_SIZE - len(merged_line))

    moved = False
    for i in range(GRID_SIZE):
        if direction == "left":
            new_line = merge(grid[i])
            if grid[i] != new_line:
                moved = True
            grid[i] = new_line
        elif direction == "right":
            new_line = merge(grid[i][::-1])[::-1]
            if grid[i] != new_line:
                moved = True
            grid[i] = new_line
        elif direction == "up":
            column = [grid[row][i] for row in range(GRID_SIZE)]
            new_column = merge(column)
            if column != new_column:
                moved = True
            for row in range(GRID_SIZE):
                grid[row][i] = new_column[row]
        elif direction == "down":
            column = [grid[row][i] for row in range(GRID_SIZE)][::-1]
            new_column = merge(column)[::-1]
            if column[::-1] != new_column:
                moved = True
            for row in range(GRID_SIZE):
                grid[row][i] = new_column[row]

    return moved

def add_random_tile(grid):
    empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if grid[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = 2 if random.random() < 0.9 else 4

def is_game_over(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return False
            if col < GRID_SIZE - 1 and grid[row][col] == grid[row][col + 1]:
                return False
            if row < GRID_SIZE - 1 and grid[row][col] == grid[row + 1][col]:
                return False
    return True

def game_over_screen():
    screen.fill(BACKGROUND_COLOR)
    game_over_text = title_font.render("Game Over", True, TITLE_COLOR)
    restart_text = font.render("Press any key to restart", True, TITLE_COLOR)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def main():
    while True:
        grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        add_random_tile(grid)
        add_random_tile(grid)
        score = 0

        running = True
        while running:
            draw_grid(grid, score)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        moved = move(grid, "up")
                    elif event.key == pygame.K_s:
                        moved = move(grid, "down")
                    elif event.key == pygame.K_a:
                        moved = move(grid, "left")
                    elif event.key == pygame.K_d:
                        moved = move(grid, "right")
                    elif event.key == pygame.K_z:
                        pygame.quit()
                        sys.exit()
                    else:
                        moved = False

                    if moved:
                        add_random_tile(grid)
                        score += sum(sum(row) for row in grid)
                    if is_game_over(grid):
                        running = False

        game_over_screen()

if __name__ == "__main__":
    main()
