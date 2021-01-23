from __future__ import annotations
import chess
import math
import rate
import random
from typing import Dict, Tuple, Union, List


def moves_to_center(board: chess.Board, move: chess.Move):
    return move.to_square in [chess.D4, chess.D5, chess.E4, chess.E5]


def moves_to_inner(board: chess.Board, move: chess.Move):
    return move.to_square in [chess.C3, chess.C4, chess.C5, chess.C6, chess.D3, chess.D6, chess.E3, chess.E6, chess.F3, chess.F4, chess.F5, chess.F6]


def captures(board, move):
    return board.is_capture(move)


def not_attacked(board, move):
    return not board.is_attacked_by(not board.turn, move.to_square)


def attacking(board, move):
    return len(board.attacks(move.to_square)) > 0


def label_for_sort(board, move):
    # Seeing best move early speeds up pruning.
    return (
        captures(board, move),
        not_attacked(board, move),
        attacking(board, move),
        moves_to_center(board, move),
        moves_to_inner(board, move),
    )


def sorted_legal_moves(board: chess.Board):
    # We want Trues to come first. But False < True. So negate.
    key = lambda move: tuple([not e for e in label_for_sort(board, move)])

    return sorted(board.legal_moves, key=key)


def best_move(
    board: chess.Board,
    depth: int,
    lo: float = math.inf,
    hi: float = -math.inf,
) -> Tuple[chess.Move | None, float, float, float]:

    if depth == 0:
        return (None, rate.rate_board(board), lo, hi)

    move_to_beat: chess.Move | None = None
    board_rating_to_beat = -math.inf if board.turn == chess.WHITE else math.inf

    moves = sorted_legal_moves(board)
    moves_left = len(moves)
    for move in moves:
        moves_left -= 1
        # print(label_for_sort(board, move))

        # Rate board if move was made
        board.push(move)
        (_, board_rating, lo, hi) = best_move(board, depth - 1, lo, hi)
        board.pop()

        # Remember best move
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

        # Prune when possible
        if last_turn(board) == chess.WHITE:
            if board_rating < lo:
                # Black will follow the path that leads to the lowest rating. White will not allow Black to get here if it can force a path with a higher rating.
                print("Pruned", moves_left, "moves")
                break
        else:
            if board_rating > hi:
                # Black would not let White get here
                print("Pruned", moves_left, "moves")
                break
        
    # exit(0)

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
