# This Memory Card Game includes:

# A grid of cards (3x4 by default)
# Card flipping mechanics
# Match checking
# Move counter
# Game over detection
# Restart capability

# Game Features:

# Cards are randomly distributed at the start
# Players can only flip two cards at a time
# Matched cards stay face up
# Unmatched cards automatically flip back after a short delay
# Move counter to track performance
# Game over message when all matches are found
# Press 'R' to restart after game over

import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_MARGIN = 20
ROWS = 3
COLS = 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Set up display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Memory Card Game")

class Card:
    def __init__(self, x, y, value):
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.value = value
        self.revealed = False
        self.matched = False
        self.animation_progress = 0
        self.animating = False

    def draw(self):
        # Draw card background
        if self.matched:
            color = GRAY
        else:
            color = BLUE if not self.revealed else WHITE
        
        pygame.draw.rect(window, color, self.rect)
        pygame.draw.rect(window, BLACK, self.rect, 2)

        # Draw card value if revealed
        if self.revealed:
            font = pygame.font.Font(None, 74)
            text = font.render(str(self.value), True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            window.blit(text, text_rect)

class MemoryGame:
    def __init__(self):
        self.cards = []
        self.selected_cards = []
        self.moves = 0
        self.matches = 0
        self.game_over = False
        self.init_cards()

    def init_cards(self):
        # Create pairs of cards
        values = list(range(1, (ROWS * COLS) // 2 + 1)) * 2
        random.shuffle(values)

        # Calculate starting position to center the cards
        start_x = (WINDOW_WIDTH - (COLS * (CARD_WIDTH + CARD_MARGIN))) // 2
        start_y = (WINDOW_HEIGHT - (ROWS * (CARD_HEIGHT + CARD_MARGIN))) // 2

        # Create card objects
        index = 0
        for row in range(ROWS):
            for col in range(COLS):
                x = start_x + col * (CARD_WIDTH + CARD_MARGIN)
                y = start_y + row * (CARD_HEIGHT + CARD_MARGIN)
                self.cards.append(Card(x, y, values[index]))
                index += 1

    def handle_click(self, pos):
        if len(self.selected_cards) >= 2:
            return

        for card in self.cards:
            if card.rect.collidepoint(pos) and not card.revealed and not card.matched:
                card.revealed = True
                self.selected_cards.append(card)
                
                if len(self.selected_cards) == 2:
                    self.moves += 1
                    if self.selected_cards[0].value == self.selected_cards[1].value:
                        self.selected_cards[0].matched = True
                        self.selected_cards[1].matched = True
                        self.matches += 1
                        self.selected_cards = []
                        
                        if self.matches == (ROWS * COLS) // 2:
                            self.game_over = True
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def hide_unmatched(self):
        for card in self.selected_cards:
            if not card.matched:
                card.revealed = False
        self.selected_cards = []

    def draw(self):
        window.fill(GRAY)
        
        # Draw all cards
        for card in self.cards:
            card.draw()

        # Draw moves counter
        font = pygame.font.Font(None, 36)
        moves_text = font.render(f"Moves: {self.moves}", True, BLACK)
        window.blit(moves_text, (10, 10))

        # Draw game over message
        if self.game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over!", True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            window.blit(text, text_rect)

def main():
    game = MemoryGame()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                game.handle_click(event.pos)
            elif event.type == pygame.USEREVENT:
                game.hide_unmatched()
                pygame.time.set_timer(pygame.USEREVENT, 0)
            elif event.type == pygame.KEYDOWN and game.game_over:
                if event.key == pygame.K_r:
                    game = MemoryGame()

        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
