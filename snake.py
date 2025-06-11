import  pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (255, 165, 0)
# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 25)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, BLUE, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food(position):
    pygame.draw.rect(screen, BLACK, (*position, CELL_SIZE, CELL_SIZE))

def show_score(score):
    score_surface = font.render(f'Score: {score}', True, GREEN)
    screen.blit(score_surface, (10, 10))

def main():
    while True:
        snake = [(100, 100), (80, 100), (60, 100)]
        direction = (CELL_SIZE, 0)
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        score = 0
        running = True
        speed = 8  # Start slower
        game_over = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and direction != (0, CELL_SIZE):
                        direction = (0, -CELL_SIZE)
                    elif event.key == pygame.K_s and direction != (0, -CELL_SIZE):
                        direction = (0, CELL_SIZE)
                    elif event.key == pygame.K_a and direction != (CELL_SIZE, 0):
                        direction = (-CELL_SIZE, 0)
                    elif event.key == pygame.K_d and direction != (-CELL_SIZE, 0):
                        direction = (CELL_SIZE, 0)

            # Move snake
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            snake.insert(0, new_head)

            # Check for collision with food
            if new_head == food:
                score += 1
                food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            else:
                snake.pop()

            # Check for collision with walls or self
            if (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake[1:]
            ):
                running = False
                game_over = True

            # Increase speed as snake grows
            speed = 8 + (len(snake) // 5)

            screen.fill(WHITE)
            draw_snake(snake)
            draw_food(food)
            show_score(score)
            pygame.display.flip()
            clock.tick(speed)

        if game_over:
            show_game_over(score)
            pygame.display.flip()
            wait_for_restart()

def show_game_over(score):
    game_over_surface = font.render(f'Game Over! Score: {score}', True, BLACK)
    restart_surface = font.render('Press SPACE to restart or ESC to quit', True, BLACK)
    screen.fill(BLUE)
    screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 + 10))


def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.time.wait(100)

if __name__ == '__main__':
    main()
