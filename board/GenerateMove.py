from board.GameState import GameState
from board.Move import Move
direction_offset = {8, -8, -1, 1, 7, -7, 9, -9}


def get_valid_moves(gamestate, white_to_move):
    return get_all_moves(gamestate, white_to_move)


def get_all_moves(gamestate: GameState, white_to_move: bool):
    moves = []
    for num in range(64):
        piece = gamestate.piece_on_square(num)
        if (piece[0] == "w" and white_to_move) or (piece[0] == "b" and not white_to_move):
            if piece[1] == "P":
                get_pawn_moves()
            elif piece[1] == "N":
                get_knight_moves()
            elif piece[1] == "B":
                get_bishop_moves()
            elif piece[1] == "R":
                get_rook_moves()
            elif piece[1] == "Q":
                get_queen_moves()
            elif piece[1] == "K":
                get_king_moves()

    return moves


def get_pawn_moves():
    pass


def get_knight_moves():
    pass


def get_bishop_moves():
    pass


def get_rook_moves():
    pass


def get_queen_moves():
    pass


def get_king_moves():
    pass


def generate_sliding_move(start_square: int, piece: str):
    if piece[1] == "Q":
        pass
