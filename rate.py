from __future__ import annotations
import chess
import math
import rate
import random
from typing import Dict, Tuple, Union

def best_move(board: chess.Board, depth: int, rating_to_beat: float) -> Tuple[chess.Move | None, float]:
    result = (None, rating_to_beat)

    moves = random.sample(list(board.legal_moves), board.legal_moves.count())

    for move in moves:
        rating = rate_move(move, board, depth, result[1])

        if rating >= result[1]:
            result = (move, rating)
    
    return result

def rate_move(move: chess.Move, board: chess.Board, depth: int, rating_to_beat: float) -> float:
    board.push(move)

    intermediate_rating = -rate.rate_board(board)
    if depth == 1:
        result = intermediate_rating
    elif intermediate_rating <= rating_to_beat:
        result = -math.inf
    else:
        (_, rating) = best_move(board, depth - 1, -intermediate_rating)
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

def rate_board(board: chess.Board) -> float:
    # Rates board for current player. > 0 favors white. Remember to invert the result if you want to rate the other player's last move from their perspective.

    if board.is_checkmate():
        result = -math.inf

    else:
        result = 0
        for square in chess.SQUARES:
            result += rate_square(board, square)
    
    return result if board.turn == chess.WHITE else -result
