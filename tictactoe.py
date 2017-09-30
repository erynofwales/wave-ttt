from flask import Flask, abort, request

BOARD_SIZE = 9

app = Flask(__name__)

class Board:
    Empty = ' '
    X = 'x'
    O = 'o'

    def __init__(self, string):
        if string is None or not isinstance(string, str):
            raise ValueError('invalid board spec')
        if len(string) != BOARD_SIZE:
            raise ValueError('board spec should be {} characters long'.format(BOARD_SIZE))

        # Process the board into an array.
        self.board = string.lower()
    
    @property
    def is_o_turn(self):
        num_x, num_o = self._tally_pieces()
        empty_board = (num_x == 0 and num_o == 0)
        full_board = (num_x + num_o == BOARD_SIZE)
        x_ahead_one = (num_x == num_o + 1)
        return (empty_board or x_ahead_one) and not full_board

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
        return "<Board:'{}'>".format(self.board)

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
        return ("Invalid board.", 400, {'Content-type': 'text/plain'})

    if not board.is_o_turn:
        return ("It isn't O's turn.\n\n{}".format(board), 400, {'Content-type': 'text/plain'})

    return (str(board), 200, {'Content-type': 'text/plain'})
