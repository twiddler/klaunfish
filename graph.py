import chess
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


def square_color(square: chess.Square):
    return "gray" if square % 2 == 0 else "#C5C5C5"


def to_node(board: chess.Board):
    return board.fen(), {"color": "blue"}


def to_edge(board: chess.Board, move: chess.Move):
    piece = board.piece_at(move.from_square)
    return (
        board.fen(),
        play(board, move).fen(),
        {"label": f"{piece}: {move.uci()}"},
    )


def turn_color(board: chess.Board):
    return "gray" if board.turn == chess.BLACK else "#C5C5C5"


def play(board: chess.Board, move: chess.Move):
    next_board = board.copy(stack=False)
    next_board.push(move)
    return next_board


def add_layer(graph, board: chess.Board, depth: int):
    if depth == 0:
        return

    moves = list(board.legal_moves)

    edges = [to_edge(board, move) for move in moves]
    graph.add_edges_from(edges)

    if depth == 3:
        non_pruned_moves = board.legal_moves
    else:
        non_pruned_moves = np.random.choice(list(board.legal_moves), 5, replace=False)

    for move in non_pruned_moves:
        board.push(move)
        add_layer(graph, board, depth - 1)
        board.pop()


def plot(graph, save_as=None, prog="twopi"):
    pos = graphviz_layout(graph, prog=prog)  # prog="dot" for top-down tree
    plt.figure(1, figsize=(20, 20))
    # colors = [turn_color(chess.Board(fen)) for fen, _ in graph.nodes.data()]
    print(graph.edges.data())
    nx.draw(graph, pos, node_size=100, width=1)  # , #node_color=colors)

    plt.axis("off")
    if save_as is not None:
        plt.savefig(save_as)
    else:
        plt.show()