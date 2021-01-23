# Make this bot compatible with https://github.com/namin/lichess-bot

from oi import auto_move_rec

def klaunfish(board):
    return auto_move_rec(board, 30).uci()

strategies = {
    "klaunfish": klaunfish
}