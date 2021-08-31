X = "X"
O = "O"
EMPTY = None

board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for line in board:
        for cell in line:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

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
    actions = set()
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
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    elif winning_player == None:
        return 0


'''
print(player(board))

print(actions(board))

print(result(board, (1, 2)))

print(winner(board))

print(terminal(board))

print(utility(board))
'''


def first_available(board):
    # Play in the first open space
    for line_index, line in enumerate(board):
        for cell_index, cell in enumerate(line):
            if cell == EMPTY:
                return (line_index, cell_index)


def win_if_possible(board):
    # Determine current player
    current_player = player(board)
    # Prepare to store actions and their utility
    utilities = []
    possible_actions = []
    # Get utility for each action
    for action in actions(board):
        action_result = result(board, action)
        action_utility = utility(action_result)
        utilities.append(action_utility)
        possible_actions.append(action)

    # Return best action based on player
    if current_player == X:
        return possible_actions[utilities.index(max(utilities))]
    elif current_player == O:
        return possible_actions[utilities.index(min(utilities))]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    print(">------------------------------------<")
    action_list = []
    utility_list = []
    if player(board) == X:
        actions_list = actions(board)
        if len(actions_list) == 9:
            return (0, 0)
        for action in actions_list:
            res = result(board, action)
            util = min_value(res)
            print(res, util_to_eng(util))
            if util == 1:
                return action
            action_list.append(action)
            utility_list.append(util)
        return action_list[utility_list.index(max(utility_list))]
    else:
        for action in actions(board):
            res = result(board, action)
            util = max_value(res)
            print(res, util_to_eng(util))
            if util == -1:
                return action
            action_list.append(action)
            utility_list.append(util)
        return action_list[utility_list.index(min(utility_list))]


def max_value(board):
    v = float('-inf')
    if terminal(board):
        return utility(board)
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
