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

    def format(self):
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
        abort(400)

    return (board.format(), 200, {'Content-type': 'text/plain'})
