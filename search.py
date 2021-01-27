from __future__ import annotations
import chess
import math
import rate
import random
from typing import Tuple, List
import networkx as nx
import graph


def wins(board: chess.Board, move: chess.Move):
    board.push(move)
    result = board.is_checkmate()
    board.pop()
    return result


def moves_to_center(board: chess.Board, move: chess.Move):
    return move.to_square in [chess.D4, chess.D5, chess.E4, chess.E5]


def moves_to_inner(board: chess.Board, move: chess.Move):
    return move.to_square in [
        chess.C3,
        chess.C4,
        chess.C5,
        chess.C6,
        chess.D3,
        chess.D6,
        chess.E3,
        chess.E6,
        chess.F3,
        chess.F4,
        chess.F5,
        chess.F6,
    ]


def captures(board, move):
    return board.is_capture(move)


def not_attacked(board, move):
    return not board.is_attacked_by(not board.turn, move.to_square)


def forks(board, move):
    return len(board.attacks(move.to_square)) > 1


def gives_check(board, move):
    board.push(move)
    result = board.is_check()
    board.pop()
    return result


def protected(board, move):
    return board.is_attacked_by(board.turn, move.to_square)


def label_for_sort(board, move):
    # Seeing best move early speeds up pruning.
    return (
        wins(board, move),
        captures(board, move),
        not_attacked(board, move),
        protected(board, move),
        forks(board, move),
        gives_check(board, move),
        moves_to_center(board, move),
        moves_to_inner(board, move),
    )


def sorted_legal_moves(board: chess.Board) -> List[chess.Move]:
    # We want Trues and high numbers to come first. So negate. (False < True.)
    key = lambda move: tuple([-e for e in label_for_sort(board, move)])

    # When moves are rated the same later on, choose one at random
    shuffled = random.sample(list(board.legal_moves), board.legal_moves.count())

    return sorted(shuffled, key=key)


def sort_moves_by_rating(board: chess.Board) -> List[chess.Move]:
    ratings = []

    moves = board.legal_moves

    for move in moves:
        board.push(move)
        rating = rate.rate_board(board)
        board.pop()
        ratings.append(rating)

    rated_moves = zip(moves, ratings)

    key = lambda rated_move: -rated_move[1]

    return [move for move, _ in sorted(rated_moves, key=key)]


def best_move(
    board: chess.Board,
    depth: float,
    alpha: float = -math.inf,
    beta: float = math.inf,
    G: nx.Graph = None,
) -> Tuple[chess.Move | None, float]:

    if depth <= 0:
        return (None, rate.rate_board(board))

    moves = sorted_legal_moves(board)

    # Find checkmates at depth != 0
    if len(moves) == 0:
        return (None, rate.rate_board(board))

    # Feeling lucky
    # moves = moves[: min(len(moves), 20)]

    result = (moves[0], -math.inf)
    # result2 = result

    # Shallow descend when move is unpromising
    descends = (1,) * (len(moves) // 2 + 1) + (2,) * (len(moves) // 2)

    for move, descend in zip(moves, descends):
        if G is not None:
            prev_board = board.copy(stack=False)

        board.push(move)

        if G is not None:
            G.add_edges_from([(graph.to_edge(prev_board, move))])

        board_rating_for_opponent = best_move(board, depth - descend, -beta, -alpha, G)[
            1
        ]
        board.pop()

        board_rating = -board_rating_for_opponent
        if board_rating > result[1]:
            # result2 = result
            result = (move, board_rating)

        alpha = max(alpha, result[1])

        if alpha >= beta:
            break

    # Shuffle first two moves to avoid draw
    # if alpha == -math.inf and beta == math.inf:
    #     random_bit, temp = None, None
    #     try:
    #         if result2[1] / result[1] >= 0.95:
    #             random_bit = int(time.time()) & 0b1
    #             if random_bit == 1:
    #                 print("everyday i'm shuffelin'")
    #                 result = result2
    #     except Exception:
    #         pass

    return result + (alpha,)