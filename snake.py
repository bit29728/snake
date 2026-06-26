import random
import sys
import pygame

# Game settings
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 12

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 50, 50)


def random_food_position(snake):
    while True:
        position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        if position not in snake:
            return position


def draw_block(surface, color, position):
    rect = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)


def show_text(surface, text, size, color, center):
    font = pygame.font.SysFont(None, size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)


def game_over(surface, score):
    surface.fill(BLACK)
    show_text(surface, "Game Over", 64, RED, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    show_text(surface, f"Length: {score}", 40, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    show_text(surface, "Press R to restart or Q to quit", 28, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = random_food_position(snake)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    direction = (1, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
            or new_head in snake
        ):
            game_over(screen, len(snake))
            snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2)]
            direction = (1, 0)
            food = random_food_position(snake)
            continue

        snake.insert(0, new_head)

        if new_head == food:
            food = random_food_position(snake)
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_block(screen, RED, food)

        for segment in snake:
            draw_block(screen, GREEN if segment == snake[0] else DARK_GREEN, segment)

        show_text(screen, f"Length: {len(snake)}", 24, WHITE, (80, 20))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
