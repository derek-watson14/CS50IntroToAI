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
        raise IndexError("This space is already taken.")

    return(board_copy)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # horizontal
    if board[0][0] != None and board[0][0] == board[0][1] == board[0][2]:
        return board[0][0]
    elif board[1][0] != None and board[1][0] == board[1][1] == board[1][2]:
        return board[1][0]
    elif board[2][0] != None and board[2][0] == board[2][1] == board[2][2]:
        return board[2][0]
    # vertical
    elif board[0][0] != None and board[0][0] == board[1][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] != None and board[0][1] == board[1][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] != None and board[0][2] == board[1][2] == board[2][2]:
        return board[0][2]
    # diagonal
    elif board[0][0] != None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] != None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    # no winner
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If someone won, board is terminal
    if winner(board) is not None:
        return True

    # If there are no more open cells, board is terminal
    full_board = True
    for line in board:
        for cell in line:
            if cell == EMPTY:
                full_board = False
                break

    return full_board


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Determine winner, or lack thereof
    winning_player = winner(board)
    # Assign a utility score to the result
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    elif winning_player == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    print("\n>------------------------------------------------<")
    print("Evaluating possible moves...")
    # Prepare to store possible actions and utility of each
    action_list = []
    utility_list = []

    # If current player is the MAX player
    if player(board) == X:
        # Get all possible actions
        actions_list = actions(board)

        # If this is the first move overall, all squares have equal utility
        if len(actions_list) == 9:
            print("(0, 0) All first moves have same utility")
            return (0, 0)

        # Loop through actions, calculate minimum (worst-case) utility
        for action in actions_list:
            util = min_value(result(board, action))
            print(action, util_to_eng(util))
            # If move will win game, stop checking other actions
            if util == 1:
                return action
            # Add action and utility to record
            action_list.append(action)
            utility_list.append(util)

        # Return the best possible option for player X based on utility
        return action_list[utility_list.index(max(utility_list))]

    # If current player is the MIN player
    else:
        actions_list = actions(board)

        for action in actions_list:
            util = max_value(result(board, action))
            print(action, util_to_eng(util))
            if util == -1:
                return action
            action_list.append(action)
            utility_list.append(util)

        return action_list[utility_list.index(min(utility_list))]


def max_value(board):
    # Set value to -inf
    v = float('-inf')
    # If board is in terminal state, return utility of board
    if terminal(board):
        return utility(board)
    """
    If board is not terminal, recursively check all possible courses the game
    could take, returning the UTILITY of each terminal game state. Then on
    the way back "up" compare these utility scores, always returning the 
    largest for a set of ACTIONS. When it reaches the "top", the MAX value that
    can be attained in the game for the given BOARD is returned
    """
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    v = float('inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def util_to_eng(util):
    if util == 1:
        return "If X plays optimally, X wins"
    if util == 0:
        return "If both play optimally, tie"
    if util == -1:
        return "If O plays optimally, O wins"
