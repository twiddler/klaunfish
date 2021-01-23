from __future__ import annotations
import chess
import math
import rate
import random
from typing import Dict, Tuple, Union, List


def sorted_legal_moves(board: chess.Board):
    # Seeing best moves early speeds up pruning.

    to_key = lambda move: (
        board.is_capture(move),
        not board.is_attacked_by(not board.turn, move.to_square),
        len(board.attacks(move.to_square)) > 0,
    )

    # We want Trues to come first. But False < True. So negate.
    key = lambda move: tuple([not e for e in to_key(move)])

    return sorted(board.legal_moves, key=key)


def best_move(
    board: chess.Board,
    depth: int,
    lo: float = math.inf,
    hi: float = -math.inf,
) -> Tuple[chess.Move | None, float, float, float]:

    move_to_beat: chess.Move | None = None
    board_rating_to_beat = -math.inf if board.turn == chess.WHITE else math.inf

    prune = False
    for move in sorted_legal_moves(board):
        if prune:
            break

        # Rate board if move was made
        board.push(move)
        if depth == 0:
            board_rating = rate.rate_board(board)
        else:
            (_, board_rating, lo, hi) = best_move(board, depth - 1, hi, lo)

            if board.turn == chess.BLACK:
                if board_rating < lo:
                    # Black will follow the path that leads to the lowest rating. White will not allow Black to get here if it can force a path with a higher rating.
                    prune = True
            else:
                if board_rating > hi:
                    # Black would not let White get here
                    prune = True

        board.pop()

        if board.turn == chess.BLACK:
            if board_rating <= board_rating_to_beat:  # TODO: Make < possible
                move_to_beat = move
                board_rating_to_beat = board_rating
                lo = min(lo, board_rating)
        else:
            if board_rating >= board_rating_to_beat:  # TODO: Make > possible
                move_to_beat = move
                board_rating_to_beat = board_rating
                hi = max(hi, board_rating)

    return (move_to_beat, board_rating_to_beat, lo, hi)


def last_turn(board):
    return not board.turn


# def rate_move(
#     move: chess.Move,
#     board: chess.Board,
#     depth: int,
#     lowest_rating: float,
#     highest_rating: float,
# ) -> Tuple[float, float, float]:
#     board.push(move)


#     return (board_rating, lowest_rating, highest_rating)


piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3.25,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 3,
}


def rate_piece(piece: chess.Piece) -> float:
    piece_value = piece_values[piece.piece_type]
    return piece_value if piece.color == chess.WHITE else -piece_value


def rate_square(board: chess.Board, square: chess.Square) -> float:
    piece = board.piece_at(square)
    return rate_piece(piece) if piece != None else 0


def rate_board(board: chess.Board) -> float:
    # > 0 favors white

    if board.is_checkmate():
        board_rating = -math.inf if last_turn(board) == chess.BLACK else math.inf

    else:
        board_rating = 0
        for square in chess.SQUARES:
            board_rating += rate_square(board, square)

    return board_rating
