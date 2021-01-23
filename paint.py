from colorama import Fore, Style, Back

def paint_squares_and_pieces(board_str):
    result = ""
    colors = cycle([paint_square_white, paint_square_black])

    for line in board_str.split("\n"):
        line += " "
        my_painter = painter(1, next(colors))
        for char in line:
            result += next(my_painter)(symbolify(char))

        result += "\n"
    return result

def cycle(l):
    while True:
        yield l
        l.append(l.pop(0))

def paint_square_white(s: str):
    return f"{Back.CYAN}{s}{Style.RESET_ALL}"

def paint_square_black(s: str):
    return f"{Back.BLUE}{s}{Style.RESET_ALL}"

def painter(margin: int, colors):
    while True:
        for color in colors:
            for _ in range(margin + 1):
                yield color

def paint_piece_black(s):
    return f"{Fore.BLACK}{s}"

def paint_piece_white(s):
    return f"{Fore.WHITE}{s}"

symbol_table = {
    'r': paint_piece_black("♜"),
    "n": paint_piece_black("♞"),
    "b": paint_piece_black("♝"),
    "q": paint_piece_black("♛"),
    "k": paint_piece_black("♚"),
    "p": paint_piece_black("♟"),
    "R": paint_piece_white("♜"),
    "N": paint_piece_white("♞"),
    "B": paint_piece_white("♝"),
    "Q": paint_piece_white("♛"),
    "K": paint_piece_white("♚"),
    "P": paint_piece_white("♟"),
    ".": " ",
    " ": " "
}

def symbolify(c):
    return symbol_table[c]
