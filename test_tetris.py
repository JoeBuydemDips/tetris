import unittest
from unittest.mock import Mock, patch
import pygame
from constants import *
from particle import Particle
from tetromino import Tetromino
from game import Game

class TestParticle(unittest.TestCase):
    def test_particle_init(self):
        particle = Particle(100, 200, NEON_RED)
        self.assertEqual(particle.x, 100)
        self.assertEqual(particle.y, 200)
        self.assertEqual(particle.color, NEON_RED)
        self.assertEqual(particle.size, 5)
        self.assertEqual(particle.lifetime, 100)

    def test_particle_update(self):
        particle = Particle(100, 200, NEON_RED)
        initial_x, initial_y = particle.x, particle.y
        particle.update()
        self.assertNotEqual((particle.x, particle.y), (initial_x, initial_y))
        self.assertEqual(particle.lifetime, 99)

    @patch('pygame.draw.circle')
    def test_particle_draw(self, mock_draw):
        screen = Mock()
        particle = Particle(100, 200, NEON_RED)
        particle.draw(screen)
        mock_draw.assert_called_once_with(screen, NEON_RED, (100, 200), 5)

class TestTetromino(unittest.TestCase):
    def test_tetromino_init(self):
        tetromino = Tetromino(100, 200)
        self.assertEqual(tetromino.x, 100)
        self.assertEqual(tetromino.y, 200)
        self.assertIn(tetromino.shape, range(7))
        self.assertIn(tetromino.color, [NEON_GREEN, NEON_BLUE, NEON_RED, NEON_PURPLE, NEON_YELLOW, NEON_CYAN, NEON_WHITE])

    def test_tetromino_rotate(self):
        tetromino = Tetromino(100, 200)
        initial_shape = tetromino.shape
        tetromino.rotate()
        self.assertEqual(tetromino.shape, (initial_shape + 1) % 7)

    @patch('pygame.draw.rect')
    def test_tetromino_draw(self, mock_draw):
        screen = Mock()
        tetromino = Tetromino(100, 200)
        tetromino.draw(screen)
        self.assertGreater(mock_draw.call_count, 0)

class TestGame(unittest.TestCase):
    @patch('pygame.display.set_mode')
    @patch('pygame.font.Font')
    def setUp(self, mock_font, mock_set_mode):
        self.game = Game()

    def test_game_init(self):
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.high_score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.lines_cleared, 0)
        self.assertFalse(self.game.game_over)

    def test_new_piece(self):
        self.game.new_piece()
        self.assertIsInstance(self.game.current_piece, Tetromino)

    def test_is_collision(self):
        self.game.current_piece = Mock()
        self.game.current_piece.shape = [[1]]
        self.game.current_piece.x = 0
        self.game.current_piece.y = 19
        self.game.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.assertTrue(self.game.is_collision())

    def test_valid_move(self):
        piece = Mock()
        piece.shape = 0
        self.assertTrue(self.game.valid_move(piece, 5, 5))
        self.assertFalse(self.game.valid_move(piece, -1, 5))

    @patch('pygame.draw.rect')
    @patch('pygame.Surface')
    def test_draw(self, mock_surface, mock_draw):
        self.game.current_piece = Mock()
        self.game.draw()
        self.assertGreater(mock_draw.call_count, 0)

    @patch('pygame.event.get')
    @patch('pygame.display.flip')
    def test_run(self, mock_flip, mock_event_get):
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]
        self.game.run()
        mock_flip.assert_called()

if __name__ == '__main__':
    unittest.main()