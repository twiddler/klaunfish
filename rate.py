import chess
import math
from typing import Dict

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
