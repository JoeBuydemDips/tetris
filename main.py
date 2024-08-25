import pygame
from game import Game

def main():
    print("Starting the game...")
    pygame.init()
    print("Pygame initialized")
    game = Game()
    print("Game instance created")
    game.run()
    print("Game finished running")

if __name__ == "__main__":
    main()