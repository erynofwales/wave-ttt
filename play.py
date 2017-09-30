#!/usr/bin/env python3

import sys
import pprint

from tictactoe import Board

start = Board(sys.argv[1])
start_score = start.evaluate()
print('Start:\n{}\n\nScore: {}'.format(start, start_score))
print('\nChildren:')
pprint.pprint(list(reversed(sorted(start.children, key=lambda b: b.score))))

print('\nNext move:\n{}'.format(start.move()))
