from __future__ import annotations
import chess
import math
import rate
import random
from typing import Dict, Tuple, Union

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

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3.25,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 3
}

def rate_piece(piece: chess.Piece) -> float:
    piece_value = piece_values[piece.piece_type]
    return piece_value if piece.color == chess.WHITE else -piece_value

def rate_square(board: chess.Board, square: chess.Square) -> float:
    piece = board.piece_at(square)
    return rate_piece(piece) if piece != None else 0

def rate_board(board: chess.Board, for_white: bool) -> float:
    # > 0 favors white

    if board.is_checkmate():
        return -math.inf if for_white else math.inf

    result = 0
    for square in chess.SQUARES:
        result += rate_square(board, square)

    return result if for_white else -result
