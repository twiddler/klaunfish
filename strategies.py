# Makes this bot compatible with https://github.com/namin/lichess-bot

from rate import best_move
import math


def klaunfish(board):
    (move, _) = best_move(board, 30)
    return move.uci()


strategies = {"klaunfish": klaunfish}
