import chess
from colorama import Fore
from colorama import Style
from colorama import Back

import negamax

def error(message: str):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")

def info(message: str):
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def player_string(is_white):
    if is_white:
        return f"{Back.WHITE}{Fore.BLACK} white {Style.RESET_ALL}"
    else:
        return f"{Back.BLACK}{Fore.WHITE} black {Style.RESET_ALL}"

def play_move_for_opponent(board, is_white):
    uci = input(f"Which move to play for {player_string(is_white)}? ")
    try:
        board.push_san(uci)
        print("")
        print(board, "\n")
    except ValueError:
        error("Not a (legal) move. Try again!\n")
        play_move_for_opponent(board, is_white)

if __name__ == "__main__":
    board = chess.Board()
    i_am_white = False

    while(True):

        play_move_for_opponent(board, not i_am_white)

        print(f"Calculating best move for {player_string(i_am_white)} ...")
        (move, rating) = negamax.best_move(board, i_am_white, 1)

        if move == None:
            info(f"No legal move left.")
            exit(0)

        board.push(move)
        print("")
        print(board, "\n")
