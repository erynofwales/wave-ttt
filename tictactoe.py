import os
from flask import Flask, abort, request

BOARD_SIZE = 9

app = Flask(__name__)

class Board:
    Empty = ' '
    X = 'x'
    O = 'o'

    def __init__(self, string='         '):
        if string is None or not isinstance(string, str):
            raise ValueError('invalid board spec')
        if len(string) != BOARD_SIZE:
            raise ValueError('board spec should be {} characters long'.format(BOARD_SIZE))

        # Process the board into an array.
        self.board = string.lower()

        num_x, num_o = self._tally_pieces()
        self.num_x = num_x
        self.num_o = num_o

        self.score = None
        self._children = None

    @property
    def empty(self):
        return self.num_x == 0 and self.num_o == 0

    @property
    def full(self):
        return self.num_x + self.num_o == BOARD_SIZE

    @property
    def is_o_turn(self):
        x_ahead_one = (self.num_x == self.num_o + 1)
        return x_ahead_one and not self.full and self.winner is None

    @property
    def next_player(self):
        if self.full:
            return None
        else:
            x_ahead_one = (self.num_x == self.num_o + 1)
            return Board.O if x_ahead_one else Board.X

    @property
    def winner(self):
        '''
        Determines if this board is a winning state, and which player won if so.
        '''
        b = self.board

        def __check(s):
            if s == 'xxx':
                return Board.X
            elif s == 'ooo':
                return Board.O
            else:
                return None

        # Check rows.
        for i in range(0, 9, 3):
            row = b[i:i+3]
            result = __check(row)
            if result:
                return result

        # Check columns.
        for i in range(0, 3):
            col = b[i] + b[i+3] + b[i+6]
            result = __check(col)
            if result:
                return result

        # Check diagonals.
        for x,y,z in ((0, 4, 8), (2, 4, 6)):
            diag = b[x] + b[y] + b[z]
            result = __check(diag)
            if result:
                return result

        return None

    @property
    def children(self):
        if self._children is None:
            self._children = list(self.iterate_children())
        return self._children

    def evaluate(self):
        '''
        Minimax algorithm, implemented recursively, to evaluate board state and
        make a move.
        '''
        score = None
        winner = self.winner
        if winner == Board.O:
            score = 1
        elif winner == Board.X:
            score = -1
        elif self.full:
            score = 0
        else:
            minmax = max if self.is_o_turn else min
            score = minmax([c.evaluate() for c in self.children])
            self._children.sort(key=lambda b: b.score, reverse=True)

        self.score = score
        return self.score

    def iterate_children(self):
        next_player = self.next_player
        if not next_player:
            yield None
        for i in range(BOARD_SIZE):
            if self.board[i] == ' ':
                b = self.board[0:i] + next_player + self.board[i+1:len(self.board)]
                yield Board(b)

    def move(self):
        self.evaluate()
        try:
            return self.children[0]
        except IndexError:
            return None

    def _tally_pieces(self):
        num_x = 0
        num_o = 0
        for c in self.board:
            if c == Board.X:
                num_x += 1
            elif c == Board.O:
                num_o += 1
        return num_x, num_o

    def __repr__(self):
        out = "<Board:'{}'".format(self.board)
        if self.score is not None:
            out += ', score:{}'.format(self.score)
        out += '>'
        return out

    def __str__(self):
        out = ''
        board_len = len(self.board)
        for x in range(board_len):
            out += self.board[x]
            x_mod = x % 3
            if x_mod == 0 or x_mod == 1:
                out += '|'
            elif x_mod == 2 and x != (board_len - 1):
                out += '\n-+-+-\n'
        return out

@app.route('/')
def hello():
    try:
        board = Board(request.args.get('board', None))
    except ValueError:
        out = 'Invalid board.'
        out += "\n\nPass a 'board' parameter to define the board, e.g. x+o++oxo+"
        return (out, 400, {'Content-type': 'text/plain'})

    if not board.is_o_turn:
        return ("It isn't O's turn.\n\n{}".format(board), 400, {'Content-type': 'text/plain'})

    next_board = board.move()

    try:
        debug = bool(int(os.environ.get('TTT_DEBUG', 0)))
    except ValueError:
        debug = False
    if debug:
        import pprint
        out = str(next_board)
        out += '\n\n---------- DEBUG ----------'
        out += '\n\nInput:\n{}'.format(board)
        out += '\n\nScore: {}'.format(board.score)
        out += '\n\nChildren:\n{}'.format(pprint.pformat(board.children))
    else:
        out = next_board.board

    return (out, 200, {'Content-type': 'text/plain'})
