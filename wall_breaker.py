import pygame
import sys
import random

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 60, 10
BALL_DIAMETER = 10
BALL_VELOCITY = 3  # Increase the ball velocity
BRICK_WIDTH, BRICK_HEIGHT = 60, 15
PADDLE_SPEED = 2

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def set_difficulty(level):
    global BALL_VELOCITY, PADDLE_SPEED
    if level == 1:
        BALL_VELOCITY = 3
        PADDLE_SPEED = 2
    elif level == 2:
        BALL_VELOCITY = 4
        PADDLE_SPEED = 3
    elif level == 3:
        BALL_VELOCITY = 5
        PADDLE_SPEED = 4

def generate_start_position():
    while True:
        pos = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT // 2)
        ball_rect = pygame.Rect(*pos, BALL_DIAMETER, BALL_DIAMETER)
        if not any(ball_rect.colliderect(pygame.Rect(i * (BRICK_WIDTH + 1), j * (BRICK_HEIGHT + 1), BRICK_WIDTH, BRICK_HEIGHT)) for i in range(0, SCREEN_WIDTH // (BRICK_WIDTH + 1)) for j in range(0, 5)):
            return pos

# Set up assets
paddle = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(*generate_start_position(), BALL_DIAMETER, BALL_DIAMETER)  # Random starting position
ball_dx = ball_dy = BALL_VELOCITY
bricks = [pygame.Rect(i * (BRICK_WIDTH + 1), j * (BRICK_HEIGHT + 1), BRICK_WIDTH, BRICK_HEIGHT) for i in range(0, SCREEN_WIDTH // (BRICK_WIDTH + 1)) for j in range(0, 5)]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.right += PADDLE_SPEED

    # Move ball
    ball.left += ball_dx
    ball.top += ball_dy

    # Collide with edges
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_dx *= -1
    if ball.top <= 0:
        ball_dy *= -1
    if ball.colliderect(paddle):
        ball_dy *= -1

    # Collide with bricks
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        hit_brick = bricks.pop(hit_index)
        ball_dy *= -1

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.rect(screen, WHITE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)

    # Flip display
    pygame.display.flip()

    # Pause
    pygame.time.wait(10)

    # if lose or ball goes out of screen, or hits all bricks, stop then restart
    if ball.top >= SCREEN_HEIGHT:
        ball.left, ball.top = generate_start_position()  # Random starting position
        ball_dx = ball_dy = BALL_VELOCITY
        bricks = [pygame.Rect(i * (BRICK_WIDTH + 1), j * (BRICK_HEIGHT + 1), BRICK_WIDTH, BRICK_HEIGHT) for i in range(0, SCREEN_WIDTH // (BRICK_WIDTH + 1)) for j in range(0, 5)]
