# Makes this bot compatible with https://github.com/namin/lichess-bot

from search import best_move
import math
import chess
import time


def dynamic_depth(board, min_depth=4):
    piece_count = sum(
        [0 if not board.piece_at(square) else 1 for square in chess.SQUARES]
    )
    dynamic_depth = max(min_depth, int(20 * math.log(2, piece_count)))
    print(f"{piece_count} pieces => go {dynamic_depth} deep")
    return dynamic_depth


def klaunfish(board):

    depth = 5
    start = time.time()
    move, rating, _ = best_move(board, depth)
    end = time.time()

    print(f"score: {rating}  ({end - start:.1f}s)")

    return move.uci()


strategies = {"klaunfish": klaunfish}
