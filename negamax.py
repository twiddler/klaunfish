import math

def best_move(board, forWhite: bool, depth: int):
    result = [None, -math.inf]
    moves = legal_moves(board, forWhite)

    for move in moves:
        rating = rate_move(move, board, forWhite, depth)

        if rating > result[0]:
            result = [move, rating]
    
    return result

def rate_move(move, board, forWhite: bool, depth: int) -> float:
    next_board = play(move, board)

    if depth == 1:
        return rate_board(next_board, forWhite)
    else:
        return -best_move(board, not forWhite, depth - 1)[1]

def rate_board(board, forWhite: bool) -> float:
    white_pieces_value = 1
    black_pieces_value = 3
    rating_for_white = white_pieces_value - black_pieces_value

    return rating_for_white if forWhite else -rating_for_white
