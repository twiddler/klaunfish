import chess
import math
from colorama import Fore, Style, Back
import inquirer
from enum import Flag
import search
import paint
import networkx as nx
import graph


class Player(Flag):
    COMPUTER = True
    HUMAN = False


def ask_player_type(color: chess.Color) -> Player:
    questions = [
        inquirer.List(
            "pieces",
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


def auto_move(board: chess.Board, depth, plot=False):
    print(f"Calculating best move for {player_string(board.turn)} ...")

    if plot:
        G = nx.DiGraph()
        move = search.best_move(board, depth, G=G)[0]
        graph.plot(G, save_as=f"depth_{depth}_{len(list(G.edges()))}_sort9.pdf")
        exit(1)
    else:
        move = search.best_move(board, depth)[0]

    if move == None:
        info(f"No legal move left.")
        exit(0)

    board.push(move)
    print("")
    print_board(board)


def print_board(board: chess.Board):
    painted = paint.paint_squares_and_pieces(str(board))
    print(painted, "\n")
