import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game objects
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED = 7

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0
        self.speed = PADDLE_SPEED

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if not up and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, 
                              HEIGHT//2 - BALL_SIZE//2, 
                              BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-1, 1])

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball collision with top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-1, 1])

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    
    # Create game objects
    left_paddle = Paddle(50, HEIGHT//2 - PADDLE_HEIGHT//2)
    right_paddle = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
    ball = Ball()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keyboard state
        keys = pygame.key.get_pressed()
        
        # Move left paddle (W and S keys)
        if keys[pygame.K_w]:
            left_paddle.move(up=True)
        if keys[pygame.K_s]:
            left_paddle.move(up=False)
            
        # Move right paddle (Up and Down arrows)
        if keys[pygame.K_UP]:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN]:
            right_paddle.move(up=False)

        # Move ball
        ball.move()

        # Ball collision with paddles
        if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
            ball.speed_x *= -1

        # Score points
        if ball.rect.left <= 0:
            right_paddle.score += 1
            ball.reset()
        elif ball.rect.right >= WIDTH:
            left_paddle.score += 1
            ball.reset()

        # Clear screen
        window.fill(BLACK)

        # Draw center line
        pygame.draw.line(window, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)

        # Draw game objects
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()

        # Draw scores
        left_score = font.render(str(left_paddle.score), True, WHITE)
        right_score = font.render(str(right_paddle.score), True, WHITE)
        window.blit(left_score, (WIDTH//4, 20))
        window.blit(right_score, (3*WIDTH//4, 20))

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


#     This Pong game includes:

# Two paddles controlled by different keys:

# Left paddle: W (up) and S (down)
# Right paddle: Up Arrow and Down Arrow


# Automatic ball movement with randomized initial direction
# Score tracking for both players
# Collision detection
# Center line for visual separation
# Smooth paddle movement
# Ball reset after scoring

# To run the game:

# Make sure you have Python installed
# Install Pygame by running pip install pygame in your command prompt
# Save the code in a file with a .py extension (e.g., pong.py)
# Run the file using Python

# The game features:

# Responsive controls
# Score display at the top of the screen
# Ball speed increases slightly after each paddle hit
# Clean visual design with white elements on black background
