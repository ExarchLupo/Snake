import  pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
OCEAN = (0, 125, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 25)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, OCEAN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_ai_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, RED, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food(position):
    pygame.draw.rect(screen, YELLOW, (*position, CELL_SIZE, CELL_SIZE))

def draw_superfood(position):
    pygame.draw.rect(screen, CYAN, (*position, CELL_SIZE, CELL_SIZE))

def draw_poison(position):
    pygame.draw.rect(screen, GREEN, (*position, CELL_SIZE, CELL_SIZE))

def draw_teleport(position):
    pygame.draw.rect(screen, MAGENTA, (*position, CELL_SIZE, CELL_SIZE))

def ai_find_nearest_food(snake_head, foods, superfood, teleport):
    """Find the nearest good food for AI"""
    all_good_food = foods + [superfood, teleport]
    if not all_good_food:
        return None
    
    nearest = min(all_good_food, key=lambda food: abs(snake_head[0] - food[0]) + abs(snake_head[1] - food[1]))
    return nearest

def ai_get_direction(snake, target, current_direction, all_snakes, poisons):
    """AI decision making for movement"""
    if target is None:
        return current_direction
    
    head = snake[0]
    possible_moves = []
    
    # Calculate possible directions
    moves = [
        ((CELL_SIZE, 0), (head[0] + CELL_SIZE, head[1])),   # right
        ((-CELL_SIZE, 0), (head[0] - CELL_SIZE, head[1])),  # left
        ((0, CELL_SIZE), (head[0], head[1] + CELL_SIZE)),   # down
        ((0, -CELL_SIZE), (head[0], head[1] - CELL_SIZE))   # up
    ]
    
    for direction, new_pos in moves:
        # Don't go backwards
        if direction == (-current_direction[0], -current_direction[1]):
            continue
        
        # Check if move is safe
        if (new_pos[0] < 0 or new_pos[0] >= WIDTH or 
            new_pos[1] < 0 or new_pos[1] >= HEIGHT):
            continue
        
        # Check collision with any snake
        collision = False
        for s in all_snakes:
            if new_pos in s[1:]:  # Check body, not head
                collision = True
                break
        
        if collision:
            continue
        
        # Avoid poison if possible
        if new_pos in poisons:
            continue
            
        # Calculate distance to target
        distance = abs(new_pos[0] - target[0]) + abs(new_pos[1] - target[1])
        possible_moves.append((direction, distance))
    
    # Choose best move
    if possible_moves:
        possible_moves.sort(key=lambda x: x[1])
        return possible_moves[0][0]
    
    # If no good moves, just avoid going backwards
    for direction, new_pos in moves:
        if direction != (-current_direction[0], -current_direction[1]):
            return direction
    
    return current_direction

def show_score(score, ai_score):
    score_surface = font.render(f'Player: {score}', True, OCEAN)
    ai_score_surface = font.render(f'AI: {ai_score}', True, RED)
    screen.blit(score_surface, (10, 10))
    screen.blit(ai_score_surface, (10, 40))

def main():
    while True:
        snake = [(100, 100), (80, 100), (60, 100)]
        direction = (CELL_SIZE, 0)
        
        # AI Snake
        ai_snake = [(700, 700), (680, 700), (660, 700)]
        ai_direction = (-CELL_SIZE, 0)
        
        # Create 5 normal foods
        foods = [(random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)) for _ in range(5)]
        superfood = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        # Create 5 poison foods
        poisons = [(random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)) for _ in range(5)]
        # Create teleport food
        teleport = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        score = 0
        ai_score = 0
        running = True
        speed = 8  # Start slower
        game_over = False
        winner = None  # Track who won
        dash_active = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_w or event.key == pygame.K_UP) and direction != (0, CELL_SIZE):
                        direction = (0, -CELL_SIZE)
                    elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and direction != (0, -CELL_SIZE):
                        direction = (0, CELL_SIZE)
                    elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and direction != (CELL_SIZE, 0):
                        direction = (-CELL_SIZE, 0)
                    elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and direction != (-CELL_SIZE, 0):
                        direction = (CELL_SIZE, 0)
                    elif event.key == pygame.K_SPACE:
                        dash_active = True

            # AI Snake logic
            ai_target = ai_find_nearest_food(ai_snake[0], foods, superfood, teleport)
            ai_direction = ai_get_direction(ai_snake, ai_target, ai_direction, [snake, ai_snake], poisons)

            # Move snake (normal move or dash 3 fields)
            if dash_active:
                # Jump 3 fields forward
                new_head = (snake[0][0] + direction[0] * 3, snake[0][1] + direction[1] * 3)
                dash_active = False
            else:
                # Normal move
                new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            
            snake.insert(0, new_head)

            # Move AI snake
            ai_new_head = (ai_snake[0][0] + ai_direction[0], ai_snake[0][1] + ai_direction[1])
            ai_snake.insert(0, ai_new_head)

            # Check for collision with food (Player)
            if new_head in foods:
                score += 1
                # Replace the eaten food with a new one
                food_index = foods.index(new_head)
                foods[food_index] = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            elif new_head  ==  superfood:
                score += 5
                # Grow snake by 5 segments (keep 4 extra segments, since we already added new_head)
                for _ in range(4):
                    snake.append(snake[-1])
                superfood = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            elif new_head == teleport:
                score += 2
                # Teleport snake to a random position
                new_random_x = random.randrange(0, WIDTH, CELL_SIZE)
                new_random_y = random.randrange(0, HEIGHT, CELL_SIZE)
                # Move the head to the new random position
                snake[0] = (new_random_x, new_random_y)
                # Move teleport food to a new location
                teleport = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            elif new_head in poisons:
                score -= 3
                # Shrink snake by 3 segments (remove from tail)
                for _ in range(3):
                    if len(snake) > 1:
                        snake.pop()
                # Replace the eaten poison with a new one
                poison_index = poisons.index(new_head)
                poisons[poison_index] = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
                
                # Check if snake is too short (Game Over)
                if len(snake) < 2:
                    running = False
                    game_over = True
                    winner = "AI"
            else:
                snake.pop()

            # Check for collision with food (AI Snake)
            if ai_new_head in foods:
                ai_score += 1
                # Replace the eaten food with a new one
                food_index = foods.index(ai_new_head)
                foods[food_index] = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            elif ai_new_head == superfood:
                ai_score += 5
                # Grow AI snake by 5 segments
                for _ in range(4):
                    ai_snake.append(ai_snake[-1])
                superfood = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            elif ai_new_head == teleport:
                ai_score += 2
                # Teleport AI snake to a random position
                new_random_x = random.randrange(0, WIDTH, CELL_SIZE)
                new_random_y = random.randrange(0, HEIGHT, CELL_SIZE)
                ai_snake[0] = (new_random_x, new_random_y)
                teleport = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
            elif ai_new_head in poisons:
                ai_score -= 3
                # Shrink AI snake by 3 segments
                for _ in range(3):
                    if len(ai_snake) > 1:
                        ai_snake.pop()
                poison_index = poisons.index(ai_new_head)
                poisons[poison_index] = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
                
                # Check if AI snake is too short
                if len(ai_snake) < 2:
                    running = False
                    game_over = True
                    winner = "Player"
            else:
                ai_snake.pop()

            # Check for collision with walls or self (Player)
            if (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake[1:] or
                new_head in ai_snake  # Collision with AI snake
            ):
                running = False
                game_over = True
                winner = "AI"

            # Check for collision with walls or self (AI Snake)
            if (
                ai_new_head[0] < 0 or ai_new_head[0] >= WIDTH or
                ai_new_head[1] < 0 or ai_new_head[1] >= HEIGHT or
                ai_new_head in ai_snake[1:] or
                ai_new_head in snake  # Collision with Player snake
            ):
                running = False
                game_over = True
                winner = "Player"

            # Increase speed as snake grows
            speed = 8 + len(snake) // 5 
                         

            screen.fill(BLACK)
            draw_snake(snake)
            draw_ai_snake(ai_snake)
            # Draw all normal foods
            for food in foods:
                draw_food(food)
            draw_superfood(superfood)
            draw_teleport(teleport)
            # Draw all poison foods
            for poison in poisons:
                draw_poison(poison)
            show_score(score, ai_score)
            pygame.display.flip()
            clock.tick(speed)

        if game_over:
            show_game_over(score, ai_score, winner)
            pygame.display.flip()
            wait_for_restart()

def show_game_over(player_score, ai_score, winner):
    screen.fill(BLACK)
    
    if winner == "Player":
        winner_surface = font.render('PLAYER WINS!', True, OCEAN)
        winner_color = OCEAN
    else:
        winner_surface = font.render('AI WINS!', True, RED)
        winner_color = RED
    
    score_surface = font.render(f'Player Score: {player_score}', True, OCEAN)
    ai_score_surface = font.render(f'AI Score: {ai_score}', True, RED)
    restart_surface = font.render('Press SPACE to restart or ESC to quit', True, WHITE)
    
    screen.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(ai_score_surface, (WIDTH // 2 - ai_score_surface.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 + 60))


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
