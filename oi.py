import chess
from colorama import Fore
from colorama import Style
from colorama import Back
import inquirer
from enum import Flag
import rate
import paint

class Player(Flag):
    COMPUTER = True
    HUMAN = False

def ask_player_type(is_white: bool) -> Player:
    questions = [
        inquirer.List("pieces",
            message=f"Who controls {player_string(is_white)}?",
            choices=["computer", "human"],
        )
    ]
    is_computer = inquirer.prompt(questions)["pieces"] == "computer"
    return is_computer

def input_depth():
    while True:
        try:
            return int(input("How many moves to look ahead? "))
        except:
            error("Not a number.")

def error(message: str):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")

def info(message: str):
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def player_string(is_white: bool):
    if is_white:
        return f"{Back.WHITE}{Fore.BLACK} white {Style.RESET_ALL}"
    else:
        return f"{Back.BLACK}{Fore.WHITE} black {Style.RESET_ALL}"

def input_move(board: chess.Board):
    uci = input(f"Which move to play for {player_string(board.turn)}? ")
    try:
        board.push_san(uci)
        print("")
        print_board(board)
    except ValueError:
        error("Not a (legal) move. Try again!\n")
        input_move(board)

def auto_move_rec(board: chess.Board, depth: int, i_am_white: bool):
    print(f"Calculating best move for {player_string(i_am_white)} ...")
    (move, _) = rate.best_move(board, i_am_white, depth)

    if move == None:
        info(f"No legal move left.")
        exit(0)

    board.push(move)
    print("")
    print_board(board)

def auto_move(board: chess.Board, depth = 3):
    auto_move_rec(board, depth, board.turn)

def print_board(board):
    painted = paint.paint_squares_and_pieces(str(board))
    print(painted, "\n")
