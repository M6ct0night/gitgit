import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 480, 320
CELL_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake Game")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def display_text(text, position, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

class SnakeGame:
    def __init__(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL_SIZE, 0)
        self.food = self.place_food()
        self.score = 0
        self.game_over = False

    def place_food(self):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def move_snake(self):
        if self.game_over:
            return

        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.place_food()
        else:
            self.snake.pop()

    def change_direction(self, new_direction):
        if (new_direction[0] != -self.direction[0] or self.direction[0] == 0) and (new_direction[1] != -self.direction[1] or self.direction[1] == 0):
            self.direction = new_direction

    def draw(self):
        screen.fill(BLACK)
        draw_grid()
        pygame.draw.rect(screen, RED, pygame.Rect(self.food[0], self.food[1], CELL_SIZE, CELL_SIZE))

        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        display_text(f"Score: {self.score}", (5, 5))

        if self.game_over:
            display_text("Game Over! Press Any Key to Restart", (10, HEIGHT // 2), RED)

    def restart(self):
        self.__init__()

def main():
    game = SnakeGame()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not game.game_over:
                    if event.key == pygame.K_w:
                        game.change_direction((0, -CELL_SIZE))
                    elif event.key == pygame.K_s:
                        game.change_direction((0, CELL_SIZE))
                    elif event.key == pygame.K_a:
                        game.change_direction((-CELL_SIZE, 0))
                    elif event.key == pygame.K_d:
                        game.change_direction((CELL_SIZE, 0))
                elif game.game_over:
                    game.restart()

        game.move_snake()
        game.draw()
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()

main()
