# Makes this bot compatible with https://github.com/namin/lichess-bot

from search import best_move


def klaunfish(board):
    move = best_move(board, 4)[0]
    return move.uci()


strategies = {"klaunfish": klaunfish}
