import numpy as np
from scipy import signal
import chess
from typing import Tuple, Dict
import math


def reshape(a):
    return np.reshape(a, (8, 8))


def gaussian_kernel(length=8, std=8):
    one_dimensional = signal.gaussian(length, std=std).reshape(length, 1)
    two_dimensional = np.outer(one_dimensional, one_dimensional)
    return two_dimensional


def prefer_push_kernel():
    kernel = gaussian_kernel(length=10)[0:8, 1:9]
    in_range = (kernel / kernel.max() * .2 + .8)
    return in_range


def avoid_corners_kernel():
    kernel = gaussian_kernel()
    in_range = (kernel / kernel.max() * .05 + .95)
    return in_range


def uniform_kernel():
    return np.ones((8, 8))


square_piece_weights = {
    chess.PAWN: prefer_push_kernel(),
    chess.BISHOP: uniform_kernel(),
    chess.KNIGHT: avoid_corners_kernel(),
    chess.ROOK: uniform_kernel(),
    chess.QUEEN: uniform_kernel(),
    chess.KING: uniform_kernel()
}


for piece, square_weights in square_piece_weights.items():
    square_piece_weights[piece] = (square_weights, np.flipud(reshape(square_weights)))


piece_values: Dict[int, Tuple[float, float]] = {
    chess.PAWN: (1., -1.),
    chess.BISHOP: (3., -3.),
    chess.KNIGHT: (3., -3.),
    chess.ROOK: (5., -5.),
    chess.QUEEN: (9., -9.),
    chess.KING: (3., -3.) 
}


def rate_piece(board: chess.Board, square: chess.Square, piece: chess.Piece) -> float:
    elem_pos = 0 if piece.color == board.turn else 1

    piece_value = piece_values[piece.piece_type][elem_pos]
    weight = square_piece_weights[piece.piece_type][elem_pos].flat[square]

    return piece_value * weight


def rate_square(board: chess.Board, square: chess.Square) -> float:
    piece = board.piece_at(square)
    return rate_piece(board, square, piece) if piece != None else 0


def rate_board(board: chess.Board) -> float:
    # > 0 favors white

    if board.is_checkmate():
        board_rating = -math.inf

    else:
        board_rating = 0 if board.castling_rights else .5
        for square in chess.SQUARES:
            board_rating += rate_square(board, square)

    return board_rating

