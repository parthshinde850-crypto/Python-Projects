

import pygame
import random
import sys
from pathlib import Path

# --------- CONFIG -----------
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
FPS = 12
HIGH_SCORE_FILE = Path("snake_highscore.txt")
# -----------------------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 180, 0)
RED = (200, 30, 30)
BLUE = (30, 130, 200)

font_small = pygame.font.SysFont(None, 24)
font_big = pygame.font.SysFont(None, 48)


def load_highscore():
    try:
        if HIGH_SCORE_FILE.exists():
            return int(HIGH_SCORE_FILE.read_text().strip() or 0)
    except Exception:
        pass
    return 0


def save_highscore(score):
    try:
        HIGH_SCORE_FILE.write_text(str(score))
    except Exception:
        pass


def draw_text(text, font, color, surface, x, y):
    img = font.render(text, True, color)
    rect = img.get_rect()
    rect.topleft = (x, y)
    surface.blit(img, rect)


def random_food_position():
    cols = WIDTH // CELL_SIZE
    rows = HEIGHT // CELL_SIZE
    x = random.randint(0, cols - 1) * CELL_SIZE
    y = random.randint(0, rows - 1) * CELL_SIZE
    return x, y


def main():
    highscore = load_highscore()

    # initial snake: 3 segments in the center
    snake = [(WIDTH // 2, HEIGHT // 2),
             (WIDTH // 2 - CELL_SIZE, HEIGHT // 2),
             (WIDTH // 2 - 2 * CELL_SIZE, HEIGHT // 2)]
    direction = (CELL_SIZE, 0)  # moving right
    next_direction = direction

    food = random_food_position()
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if not game_over:
                    # accept arrow keys or WASD
                    if event.key in (pygame.K_LEFT, pygame.K_a) and direction != (CELL_SIZE, 0):
                        next_direction = (-CELL_SIZE, 0)
                    if event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-CELL_SIZE, 0):
                        next_direction = (CELL_SIZE, 0)
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, CELL_SIZE):
                        next_direction = (0, -CELL_SIZE)
                    if event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -CELL_SIZE):
                        next_direction = (0, CELL_SIZE)
                else:
                    # game over controls
                    if event.key == pygame.K_r:
                        main()  # restart fresh
                        return

        if not running:
            break

        if not game_over:
            # update direction
            direction = next_direction

            # move snake: insert new head
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # wrap-around behavior (optional). If you prefer death on wall, comment the wrap and enable wall-check below.
            new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)

            snake.insert(0, new_head)

            # check if food eaten
            if new_head == food:
                score += 1
                # place new food not on the snake
                while True:
                    food = random_food_position()
                    if food not in snake:
                        break
            else:
                # remove tail
                snake.pop()

            # collision with self?
            if new_head in snake[1:]:
                game_over = True
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)

            # optional: wall collision death (if you want wall-death instead of wrap)
            # hx, hy = new_head
            # if hx < 0 or hx >= WIDTH or hy < 0 or hy >= HEIGHT:
            #     game_over = True

        # --- DRAW ---
        screen.fill(BLACK)

        # grid (optional, for looks)
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # draw food
        fx, fy = food
        pygame.draw.rect(screen, RED, (fx, fy, CELL_SIZE, CELL_SIZE))

        # draw snake
        for i, (sx, sy) in enumerate(snake):
            rect = pygame.Rect(sx, sy, CELL_SIZE, CELL_SIZE)
            if i == 0:
                pygame.draw.rect(screen, BLUE, rect)  # head
            else:
                pygame.draw.rect(screen, GREEN, rect)

        # HUD
        draw_text(f"Score: {score}", font_small, WHITE, screen, 8, 8)
        draw_text(f"Highscore: {highscore}", font_small, WHITE, screen, 8, 30)
        draw_text("Press Esc to quit", font_small, WHITE, screen, WIDTH - 150, 8)

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            draw_text("GAME OVER", font_big, WHITE, screen, WIDTH // 2 - 110, HEIGHT // 2 - 60)
            draw_text(f"Score: {score}", font_small, WHITE, screen, WIDTH // 2 - 40, HEIGHT // 2)
            draw_text("Press R to Restart or Esc to Quit", font_small, WHITE, screen, WIDTH // 2 - 140, HEIGHT // 2 + 40)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
