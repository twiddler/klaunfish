import chess
import math
from typing import Tuple, Union

def best_move(board: chess.Board, for_white: bool, depth: int) -> Tuple[Union[chess.Move, None], float]:
    result = (None, -math.inf)

    for move in board.legal_moves:
        rating = rate_move(move, board, for_white, depth)

        if rating > result[1]:
            result = (move, rating)
    
    return result

def rate_move(move: chess.Move, board: chess.Board, for_white: bool, depth: int) -> float:
    board.push(move)

    if depth == 1:
        result = rate_board(board, for_white)
    else:
        (_, rating) = best_move(board, not for_white, depth - 1)
        result = -rating

    board.pop()
    return result

def rate_board(board: chess.Board, for_white: bool) -> float:
    white_pieces_value = 1
    black_pieces_value = 3
    rating_for_white = white_pieces_value - black_pieces_value

    return rating_for_white if for_white else -rating_for_white