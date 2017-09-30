# test.py
# Eryn Wells <eryn@erynwells.me>
'''
Unit tests for tictactoe.
'''

import unittest
from tictactoe import Board

class BoardTests(unittest.TestCase):
    def test_default_is_empty(self):
        b = Board()
        self.assertTrue(b.empty)
        self.assertFalse(b.full)
        self.assertEqual(b.next_player, Board.X)

    def test_winner(self):
        wins = [
            # Rows.
            'xxx o o o',
            'oo xxxo  ',
            'o o o xxx',
            # Columns.
            'xooxo x  ',
            'oxo xo x ',
            'o xo x ox',
            # Diagonals.
            'xo ox  ox',
            'o xox x o',
        ]
        for b in wins:
            with self.subTest(board=b):
                board = Board(b)
                self.assertEqual(board.winner, Board.X, 'expected X to win\n{}'.format(board))

        table = str.maketrans('xo', 'ox')
        wins = [b.translate(table) for b in wins]
        for b in wins:
            with self.subTest(board=b):
                board = Board(b)
                self.assertEqual(board.winner, Board.O, 'expected O to win\n{}'.format(board))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
