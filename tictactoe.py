from flask import Flask, abort, request

app = Flask(__name__)

@app.route('/')
def hello():
    board = _get_board_or_abort()
    return board

def _get_board_or_abort():
    '''
    Get the board from the request, or abort the request with a 400 error.
    '''
    board = request.args.get('board', None)
    is_valid = all(
        board is not None,  # 'board' var must exist.
        len(board) >= 9,    # Board should be at least 9 characters long.
    )

    if not is_valid:
        abort(400)

    return board
