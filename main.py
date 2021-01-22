import chess
from utils import *

if __name__ == "__main__":
    board = chess.Board()
    
    depth = input_depth()
    i_am_white = ask_if_white()

    if not i_am_white:
        print("Flipped board.\n")
        print_board(board, i_am_white)
        play_move_for_opponent(board, i_am_white)
    else:
        print_board(board, i_am_white)

    while(True):
        calculate_move_for_me(board, depth, i_am_white)
        calculate_move_for_me(board, depth, not i_am_white)
        # play_move_for_opponent(board, i_am_white)