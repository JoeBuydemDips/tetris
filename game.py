import pygame
import random
from constants import *
from particle import Particle
from tetromino import Tetromino

class Game:
    def __init__(self):
        print("Initializing Game...")
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cyberpunk Tetris")
        print(f"Display mode set: {pygame.display.get_window_size()}")
        self.clock = pygame.time.Clock()
        self.grid_width = (WIDTH - SIDEBAR_WIDTH) // BLOCK_SIZE
        self.grid_height = HEIGHT // BLOCK_SIZE
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.current_piece = None
        self.score = 0
        self.game_over = False
        self.particles = []
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.high_score = 0
        self.level = 1
        self.lines_cleared = 0
        self.paused = False
        self.font_large = pygame.font.Font(None, 72)  # Larger font for pause screen
        print("Game initialized")

    def spawn_new_piece(self):
        print("Spawning new piece")
        initial_x = (self.grid_width * BLOCK_SIZE) // 2 - BLOCK_SIZE
        self.current_piece = Tetromino(initial_x, 0)
        if self.is_collision():
            print("Collision detected on spawn")
            self.game_over = True
        else:
            print("New piece spawned successfully")

    def is_collision(self):
        if not self.current_piece:
            return False
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    next_y = self.current_piece.y // BLOCK_SIZE + i
                    next_x = self.current_piece.x // BLOCK_SIZE + j
                    if (next_y >= self.grid_height or
                        next_x < 0 or next_x >= self.grid_width or
                        (next_y >= 0 and self.grid[next_y][next_x])):
                        print(f"Collision detected at x:{next_x}, y:{next_y}")
                        return True
        return False

    def new_piece(self):
        self.current_piece = Tetromino(WIDTH // 2, 0)

    def valid_move(self, piece, x, y):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    next_x = x // BLOCK_SIZE + j
                    next_y = y // BLOCK_SIZE + i
                    if (next_x < 0 or next_x >= self.grid_width or
                        next_y >= self.grid_height or
                        (next_y >= 0 and self.grid[next_y][next_x])):
                        return False
        return True

    def place_piece(self):
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y // BLOCK_SIZE + i][self.current_piece.x // BLOCK_SIZE + j] = self.current_piece.color

    def draw(self):
        self.screen.fill(NEON_BLACK)
        
        # Draw the game grid
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.grid[i][j]:
                    pygame.draw.rect(self.screen, self.grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw the current piece
        if self.current_piece:
            self.current_piece.draw(self.screen)

        # Draw sidebar
        sidebar_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, NEON_PURPLE, sidebar_rect)
        
        # Add a glow effect to the sidebar
        glow_surf = pygame.Surface((SIDEBAR_WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*GLOW_COLOR, 100), glow_surf.get_rect(), border_radius=10)
        self.screen.blit(glow_surf, (WIDTH - SIDEBAR_WIDTH, 0))

        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, NEON_GREEN)
        self.screen.blit(score_text, (WIDTH - SIDEBAR_WIDTH + 20, 20))

        # High Score
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, NEON_YELLOW)
        self.screen.blit(high_score_text, (WIDTH - SIDEBAR_WIDTH + 20, 60))

        # Level
        level_text = self.font_medium.render(f"Level: {self.level}", True, NEON_RED)
        self.screen.blit(level_text, (WIDTH - SIDEBAR_WIDTH + 20, 100))

        # Lines Cleared
        lines_text = self.font_medium.render(f"Lines: {self.lines_cleared}", True, NEON_WHITE)
        self.screen.blit(lines_text, (WIDTH - SIDEBAR_WIDTH + 20, 140))

        # Controls
        controls = [
            "Controls:",
            "Left : Move Left",
            "Right: Move Right",
            "Down : Soft Drop",
            "Up   : Rotate"
        ]
        for i, line in enumerate(controls):
            control_text = self.font_small.render(line, True, NEON_CYAN)
            self.screen.blit(control_text, (WIDTH - SIDEBAR_WIDTH + 20, 200 + i * 30))

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)

        if self.paused:
            self.draw_pause_screen()

    def draw_pause_screen(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        self.screen.blit(overlay, (0, 0))

        # Draw "PAUSED" text
        pause_text = self.font_large.render("PAUSED", True, NEON_CYAN)
        text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(pause_text, text_rect)

        # Draw instruction
        instruction_text = self.font_medium.render("Press any key to resume", True, NEON_WHITE)
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.screen.blit(instruction_text, instruction_rect)

    def run(self):
        print("Starting game loop...")
        self.spawn_new_piece()
        last_fall_time = pygame.time.get_ticks()
        fall_speed = 1000  # Time in milliseconds between each downward movement

        frame_count = 0
        while not self.game_over:
            frame_count += 1
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event received")
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif self.paused:
                        self.paused = False  # Resume on any key press
                    elif event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.current_piece.x - BLOCK_SIZE, self.current_piece.y):
                            self.current_piece.x -= BLOCK_SIZE
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.current_piece.x + BLOCK_SIZE, self.current_piece.y):
                            self.current_piece.x += BLOCK_SIZE
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + BLOCK_SIZE):
                            self.current_piece.y += BLOCK_SIZE
                    elif event.key == pygame.K_UP:
                        rotated = Tetromino(self.current_piece.x, self.current_piece.y)
                        rotated.shape = list(zip(*self.current_piece.shape[::-1]))  # Rotate
                        if self.valid_move(rotated, rotated.x, rotated.y):
                            self.current_piece.shape = rotated.shape

            if not self.paused:
                # Move piece down automatically
                if current_time - last_fall_time > fall_speed:
                    if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + BLOCK_SIZE):
                        self.current_piece.y += BLOCK_SIZE
                    else:
                        self.place_piece()
                        self.spawn_new_piece()
                    last_fall_time = current_time

                # Check for line clears
                lines_cleared = 0
                for i in range(self.grid_height - 1, -1, -1):
                    if all(self.grid[i]):
                        del self.grid[i]
                        self.grid.insert(0, [0 for _ in range(self.grid_width)])
                        lines_cleared += 1

                if lines_cleared:
                    self.score += (lines_cleared ** 2) * 100
                    self.lines_cleared += lines_cleared
                    self.level = self.lines_cleared // 10 + 1
                    self.high_score = max(self.high_score, self.score)
                    for _ in range(lines_cleared * 10):
                        self.particles.append(Particle(random.randint(0, WIDTH), random.randint(0, HEIGHT), NEON_RED))

                # Update particles
                for particle in self.particles[:]:
                    particle.update()
                    if particle.lifetime <= 0:
                        self.particles.remove(particle)

            # Draw everything
            self.draw()
            pygame.display.flip()
            if frame_count % 60 == 0:  # Print every 60 frames
                print(f"Frame updated: {frame_count}")

            # Control game speed
            self.clock.tick(FPS)

        print(f"Game over. Total frames: {frame_count}")
        # Game over screen
        game_over_text = self.font_large.render("Game Over", True, NEON_RED)
        self.screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 24))
        pygame.display.flip()
        pygame.time.wait(2000)