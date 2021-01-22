from __future__ import annotations
import chess
import math
from typing import Tuple, Union
import rate
import random

def best_move(board: chess.Board, for_white: bool, depth: int) -> Tuple[chess.Move | None, float]:
    result = (None, -math.inf)

    moves = random.sample(list(board.legal_moves), board.legal_moves.count())

    for move in moves:
        rating = rate_move(move, board, for_white, depth)

        if rating > result[1]:
            result = (move, rating)
    
    return result

def rate_move(move: chess.Move, board: chess.Board, for_white: bool, depth: int) -> float:
    board.push(move)

    if depth == 1:
        result = rate.rate_board(board, for_white)
    else:
        (_, rating) = best_move(board, not for_white, depth - 1)
        result = -rating

    board.pop()
    return result