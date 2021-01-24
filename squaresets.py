import numpy as np
from scipy import signal
import time
import matplotlib.pyplot as plt
import chess
from typing import Tuple, Dict


def reshape(a):
    return np.reshape(a, (8, 8))


def plot_weighted_board(a):
    plt.imshow(reshape(a), interpolation='none')
    plt.show()


def gaussian_kernel(length=8, std=8):
    one_dimensional = signal.gaussian(length, std=std).reshape(length, 1)
    two_dimensional = np.outer(one_dimensional, one_dimensional)
    return two_dimensional


def corner_kernel(length=16, flip: bool=False):
    return (np.fliplr if flip else lambda x: x)(gaussian_kernel(length=16, std=3)[8:16, 8:16])


def starting_corners_kernel():
    corners = (corner_kernel() + corner_kernel(flip=True))
    in_range = (corners / corners.max() * .2 + .8)
    return in_range


def prefer_push_kernel():
    kernel = gaussian_kernel(length=10)[0:8, 1:9]
    in_range = (kernel / kernel.max() * .2 + .8)
    return in_range


def avoid_corners_kernel():
    kernel = gaussian_kernel()
    in_range = (kernel / kernel.max() * .05 + .95)
    return in_range


square_piece_weights = {
    chess.PAWN: prefer_push_kernel(),
    chess.BISHOP: np.ones((8, 8)),  # TODO: better kernel
    chess.KNIGHT: avoid_corners_kernel(),
    chess.ROOK: np.ones((8, 8)),  # TODO: better kernel
    chess.QUEEN: np.ones((8, 8)),
    chess.KING: np.ones((8, 8))  # starting_corners_kernel()
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


def weighted_board(board: chess.Board):
    result = reshape(np.zeros((64,)))

    for piece, (ally_value, enemy_value) in piece_values.items():
        # Multiplying with np.array is faster than with list comprehension
        result += reshape(np.array(board.pieces(piece, board.turn).tolist())) * ally_value * square_piece_weights[piece]
        result += reshape(np.array(board.pieces(piece, not board.turn).tolist())) * enemy_value * np.flipud(square_piece_weights[piece])

    return result