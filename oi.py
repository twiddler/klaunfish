import chess
import math
from colorama import Fore, Style, Back
import inquirer
from enum import Flag
import rate
import paint

class Player(Flag):
    COMPUTER = True
    HUMAN = False

def ask_player_type(color: chess.Color) -> Player:
    questions = [
        inquirer.List("pieces",
            message=f"Who controls {player_string(color)}?",
            choices=["computer", "human"],
        )
    ]
    is_computer = inquirer.prompt(questions)["pieces"] == "computer"
    return Player.COMPUTER if is_computer else Player.HUMAN

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

def player_string(color: chess.Color):
    if color == chess.WHITE:
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

def auto_move_rec(board: chess.Board, depth: int) -> chess.Move:
    print(f"Calculating best move for {player_string(board.turn)} ...")
    (move, _) = rate.best_move(board, depth, -math.inf)

    if move == None:
        # Lichess games should not end before this happens
        info(f"No legal move left.")
        exit(0)

    return move

def auto_move(board: chess.Board, depth = 11):
    move = auto_move_rec(board, depth)

    board.push(move)
    print("")
    print_board(board)


def print_board(board: chess.Board):
    painted = paint.paint_squares_and_pieces(str(board))
    print(painted, "\n")
