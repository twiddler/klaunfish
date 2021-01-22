import chess
from utils import *

if __name__ == "__main__":
    board = chess.Board()
    
    depth = input_depth()
    i_am_white = ask_if_white()

    if not i_am_white:
        board = board.transform(chess.flip_vertical)
        print("Flipped board.\n")
        print(board, "\n")
        play_move_for_opponent(board, not i_am_white)
    else:
        print(board, "\n")

    while(True):
        calculate_move_for_me(board, depth, i_am_white)
        play_move_for_opponent(board, not i_am_white)