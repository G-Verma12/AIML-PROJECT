import pygame
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Dodge Pro")

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 40)

# Clock
clock = pygame.time.Clock()

# Player setup
player_size = 40
player_speed = 6

# Game variables
high_score = 0


# AI Difficulty Logic
def adjust_difficulty(score, speed):
    if score < 5:
        return 4
    elif score < 10:
        return 6
    elif score < 20:
        return 8
    else:
        return speed + 0.3


# Draw text helper
def draw_text(text, font, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))


# Game Loop
def game_loop():
    global high_score

    player_x = WIDTH // 2
    player_y = HEIGHT - 60

    enemy_x = random.randint(0, WIDTH - player_size)
    enemy_y = 0
    enemy_speed = 4

    score = 0
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # Move enemy
        enemy_y += enemy_speed

        if enemy_y > HEIGHT:
            enemy_y = 0
            enemy_x = random.randint(0, WIDTH - player_size)
            score += 1

            # AI adjustment
            enemy_speed = adjust_difficulty(score, enemy_speed)

        # Collision
        if (
            player_x < enemy_x + player_size and
            player_x + player_size > enemy_x and
            player_y < enemy_y + player_size and
            player_y + player_size > enemy_y
        ):
            if score > high_score:
                high_score = score
            game_over(score)
            return

        # Draw objects
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))
        pygame.draw.rect(screen, RED, (enemy_x, enemy_y, player_size, player_size))

        # Score display
        draw_text(f"Score: {score}", font, BLACK, 10, 10)
        draw_text(f"High Score: {high_score}", font, BLACK, 10, 40)

        pygame.display.update()
        clock.tick(60)


# Game Over Screen
def game_over(score):
    while True:
        screen.fill(WHITE)

        draw_text("Game Over", big_font, RED, 150, 200)
        draw_text(f"Score: {score}", font, BLACK, 180, 260)
        draw_text("Press R to Restart", font, BLACK, 130, 320)
        draw_text("Press Q to Quit", font, BLACK, 150, 360)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()


# Start Menu
def start_menu():
    while True:
        screen.fill(WHITE)

        draw_text("Smart Dodge Pro", big_font, BLACK, 100, 200)
        draw_text("Press SPACE to Start", font, BLACK, 120, 300)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()


# Start game
start_menu()