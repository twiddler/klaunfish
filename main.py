import chess
import oi # ᕕ(⌐■_■)ᕗ

if __name__ == "__main__":
    board = chess.Board()
    
    players = tuple([oi.ask_player_type(color) for color in (chess.WHITE, chess.BLACK)])

    #if oi.Player.COMPUTER in players:
    depth = oi.input_depth()

    oi.print_board(board)

    while True:
        for player in players:
            if player == oi.Player.COMPUTER:
                oi.auto_move(board, depth)
            else:
                oi.input_move(board)
