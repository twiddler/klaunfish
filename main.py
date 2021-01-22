import chess
from utils import *

if __name__ == "__main__":
    board = chess.Board()
    
    depth = input_depth()
    i_am_white = ask_if_white()

    if not i_am_white:
        print("Flipped board.\n")
        print_board(board, i_am_white)
        input_move(board, i_am_white)
    else:
        print_board(board, i_am_white)

    while(True):
        auto_move(board, depth, i_am_white)
        auto_move(board, depth, not i_am_white)
        input_move(board, i_am_white)
