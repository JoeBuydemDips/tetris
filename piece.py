import random

class Piece:
    def __init__(self):
        self.shapes = [
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]]   # Z
        ]
        self.shape = random.choice(self.shapes)
        self.color = random.randint(1, 7)
        self.x = 3
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))
