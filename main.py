import chess
from colorama import Fore
from colorama import Style
from colorama import Back

def error(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")

str_white = f"{Back.WHITE}{Fore.BLACK} white {Style.RESET_ALL}"

if __name__ == "__main__":
    board = chess.Board()

    while(True):
        uci = input(f"Which move to play for {str_white}? ")

        try:
            board.push_san(uci)
            print(board)
        except ValueError:
            error("Not a (legal) move. Try again!\n")

    
    print(bool(board.castling_rights))