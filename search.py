from __future__ import annotations
import chess
import math
import rate
import random
from typing import Tuple, List


def wins(board: chess.Board, move: chess.Move):
    board.push(move)
    result = board.is_checkmate()
    board.pop()
    return result


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
        wins(board, move),
        captures(board, move),
        not_attacked(board, move),
        attacking(board, move),
        moves_to_center(board, move),
        moves_to_inner(board, move),
    )


def sorted_legal_moves(board: chess.Board) -> List[chess.Move]:
    # We want Trues to come first. But False < True. So negate.
    key = lambda move: tuple([not e for e in label_for_sort(board, move)])

    # Don't get stuck
    shuffled = random.sample(list(board.legal_moves), board.legal_moves.count())

    return sorted(shuffled, key=key)


def best_move(
    board: chess.Board,
    depth: int,
    alpha: float = -math.inf,
    beta: float = math.inf,
) -> Tuple[chess.Move | None, float]:

    if depth == 0:
        return (None, rate.rate_board(board))

    moves = sorted_legal_moves(board)

    # Find checkmates at depth != 0
    if len(moves) == 0:
        return (None, rate.rate_board(board))
    
    result = (moves[0], -math.inf)

    moves = sorted_legal_moves(board)
    for move in moves:
        board.push(move)
        (_, board_rating_for_opponent) = best_move(board, depth-1 , -beta, -alpha)
        board.pop()

        board_rating = -board_rating_for_opponent
        if board_rating > result[1]:
            result = (move, board_rating)

        alpha = max(alpha, result[1])

        if alpha >= beta:
            break

    return result