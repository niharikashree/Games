# This Flappy Bird clone includes:

# Bird physics with gravity and jumping
# Randomly generated pipes
# Score tracking
# Collision detection
# Game over state with restart option

# Game Features:

# Press SPACE to make the bird jump
# Navigate through pipes to score points
# Game over when hitting pipes or going out of bounds
# Press SPACE to restart after game over
# Score display at the top of the screen


# Controls:

# SPACE: Jump/Restart
# Close window to quit


import pygame
import random
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_SPEED = 3
PIPE_GAP = 200
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

# Set up display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

class Bird:
    def __init__(self):
        self.x = WINDOW_WIDTH // 4
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.size = 30
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(200, WINDOW_HEIGHT - 200)
        self.x = WINDOW_WIDTH
        self.width = 70
        self.passed = False
        
        # Create rectangles for top and bottom pipes
        self.top_pipe = pygame.Rect(
            self.x,
            0,
            self.width,
            self.gap_y - PIPE_GAP // 2
        )
        self.bottom_pipe = pygame.Rect(
            self.x,
            self.gap_y + PIPE_GAP // 2,
            self.width,
            WINDOW_HEIGHT - (self.gap_y + PIPE_GAP // 2)
        )

    def update(self):
        self.x -= PIPE_SPEED
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

    def draw(self):
        pygame.draw.rect(window, GREEN, self.top_pipe)
        pygame.draw.rect(window, GREEN, self.bottom_pipe)

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.last_pipe = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 74)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__init__()  # Reset game
                    else:
                        self.bird.jump()
        return True

    def update(self):
        if self.game_over:
            return
        self.bird.update()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe > PIPE_FREQUENCY:
            self.pipes.append(Pipe())
            self.last_pipe = current_time
        for pipe in self.pipes[:]:
            pipe.update()
            if pipe.x + pipe.width < 0:
                self.pipes.remove(pipe)
                continue
            if (pipe.top_pipe.colliderect(self.bird.rect) or 
                pipe.bottom_pipe.colliderect(self.bird.rect)):
                self.game_over = True
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
        if self.bird.y < 0 or self.bird.y + self.bird.size > WINDOW_HEIGHT:
            self.game_over = True

    def draw(self):
        window.fill(SKY_BLUE)
        for pipe in self.pipes:
            pipe.draw()
        self.bird.draw()
        score_text = self.font.render(str(self.score), True, WHITE)
        window.blit(score_text, (WINDOW_WIDTH//2 - 20, 50))
        if self.game_over:
            game_over_text = self.font.render("Game Over!", True, WHITE)
            restart_text = pygame.font.Font(None, 36).render(
                "Press SPACE to restart", True, WHITE)
            window.blit(game_over_text, 
                       (WINDOW_WIDTH//2 - 140, WINDOW_HEIGHT//2 - 50))
            window.blit(restart_text, 
                       (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 20))

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        running = game.handle_input()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
