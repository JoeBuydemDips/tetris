import pygame
import random
from constants import *

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shapes = [
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            
            [[1, 1],
             [1, 1]],
            
            [[0, 1, 0],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[1, 0, 0],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[0, 0, 1],
             [1, 1, 1],
             [0, 0, 0]],
            
            [[1, 1, 0],
             [0, 1, 1],
             [0, 0, 0]],
            
            [[0, 1, 1],
             [1, 1, 0],
             [0, 0, 0]]
        ]
        self.shape = random.choice(self.shapes)
        self.color = self.get_color()

    def get_color(self):
        colors = [NEON_GREEN, NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_YELLOW, NEON_CYAN, NEON_WHITE]
        return random.choice(colors)

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

    def draw(self, screen):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, 
                                     (self.x + j * BLOCK_SIZE, 
                                      self.y + i * BLOCK_SIZE, 
                                      BLOCK_SIZE, BLOCK_SIZE))