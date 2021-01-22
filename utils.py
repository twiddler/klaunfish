import chess
from colorama import Fore
from colorama import Style
from colorama import Back
import inquirer
import negamax

def ask_if_white() -> bool:
    questions = [
        inquirer.List("pieces",
            message="Which pieces do you play?",
            choices=["white", "black"],
        )
    ]
    i_am_white = inquirer.prompt(questions)["pieces"] == "white"
    return i_am_white

def input_depth() -> int:
    while True:
        try:
            return int(input("How many moves to look ahead? "))
        except:
            error("Not a number.")

def error(message: str):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")

def info(message: str):
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def player_string(is_white: bool) -> str:
    if is_white:
        return f"{Back.WHITE}{Fore.BLACK} white {Style.RESET_ALL}"
    else:
        return f"{Back.BLACK}{Fore.WHITE} black {Style.RESET_ALL}"

def play_move_for_opponent(board: chess.Board, i_am_white: bool):
    uci = input(f"Which move to play for {player_string(not i_am_white)}? ")
    try:
        board.push_san(uci)
        print("")
        print_board(board, i_am_white)
    except ValueError:
        error("Not a (legal) move. Try again!\n")
        play_move_for_opponent(board, not i_am_white)

def calculate_move_for_me(board: chess.Board, depth: int, i_am_white: bool):
    print(f"Calculating best move for {player_string(i_am_white)} ...")
    (move, _) = negamax.best_move(board, i_am_white, depth)

    if move == None:
        info(f"No legal move left.")
        exit(0)

    board.push(move)
    print("")
    print_board(board, i_am_white)

def print_board(board, i_am_white):
    print(board if i_am_white else board.transform(chess.flip_vertical), "\n")