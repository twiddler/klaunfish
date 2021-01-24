# Makes this bot compatible with https://github.com/namin/lichess-bot

from rate import best_move
import math


def klaunfish(board):
    move = best_move(board, 5)[0]
    return move.uci()


strategies = {"klaunfish": klaunfish}
