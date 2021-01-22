import chess
import oi # ᕕ(⌐□_□)ᕗ

if __name__ == "__main__":
    board = chess.Board()
    
    depth = oi.input_depth()
    i_am_white = oi.ask_if_white()

    if not i_am_white:
        print("Flipped board.\n")
        oi.print_board(board)
        oi.input_move(board, i_am_white)
    else:
        oi.print_board(board)

    while(True):
        oi.auto_move(board, depth, i_am_white)
        oi.auto_move(board, depth, not i_am_white)
        # oi.input_move(board, i_am_white)
