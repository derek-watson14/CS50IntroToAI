"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count how many times each player has played
    x_count = 0
    o_count = 0
    for line in board:
        for cell in line:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    # Return who has the next turn
    if x_count > o_count:
        return O
    elif o_count > x_count:
        return X
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Create actions set
    actions = set()

    # Loop through board and add all empty cells to actions set
    for line_index, line in enumerate(board):
        for cell_index, cell in enumerate(line):
            if cell == EMPTY:
                actions.add((line_index, cell_index))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Deep copy board
    board_copy = [[board[0][0], board[0][1], board[0][2]],
                  [board[1][0], board[1][1], board[1][2]],
                  [board[2][0], board[2][1], board[2][2]]]

    # Make move if cell is open, else raise exception
    if board_copy[action[0]][action[1]] is None:
        board_copy[action[0]][action[1]] = player(board)
    else:
        raise IndexError("Board cell is already taken.")

    return(board_copy)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
