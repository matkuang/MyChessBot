import math
import random

from board.Move import Move
from board.GameState import GameState
from board.GenerateMove import get_valid_moves, in_check
from board.GameHistory import GameHistory

import cProfile

def minimax(depth: int, gamestate: GameState) -> (int, Move):
    if depth == 0:
        return gamestate.evaluate(), None

    moves = get_valid_moves(gamestate.colour_to_move, gamestate)
    if len(moves) == 0:
        if in_check(gamestate.colour_to_move, gamestate):
            return -math.inf, None
        else:
            return 0, None

    best_evaluation = -math.inf
    best_move = random.choice(moves)
    for move in moves:
        gamestate.make_move(move)
        current_evaluation = minimax(depth - 1, gamestate)[0] * -1
        if current_evaluation > best_evaluation:
            best_move = move
        best_evaluation = max(best_evaluation, current_evaluation)
        gamestate.unmake_move()
    return best_evaluation, best_move


if __name__ == '__main__':
    gs = GameState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", GameHistory())
    gs.make_move(Move(8, 16, "wP", "--"))
    cProfile.run('gs.make_move(Move(8, 16, "wP", "--"))')
    cProfile.run("gs.unmake_move()")
    cProfile.run("get_valid_moves('w', gs)")
    cProfile.run("minimax(3, gs)")







