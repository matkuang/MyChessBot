from board.GameState import GameState
from board.Move import Move
from board.BoardUtility import num_squares_to_edge


DIRECTION_OFFSETS = (8, -8, -1, 1, 7, -7, 9, -9)  # N S W E NW SE NE SW
SLIDING_PIECES = {"B", "R", "Q"}

def get_valid_moves(gamestate, white_to_move) -> list[Move]:
    return get_all_moves(gamestate, white_to_move)


def get_all_moves(gamestate: GameState, white_to_move: bool) -> list[Move]:
    moves = []
    for square in range(64):
        piece = gamestate.get_piece_on_square(square)
        colour = piece[0]
        if (colour == "w" and white_to_move) or (colour == "b" and not white_to_move):
            if piece[1] == "P":
                moves.extend(get_pawn_moves(colour, square, gamestate))
            elif piece[1] == "N":
                get_knight_moves()

            elif piece[1] in SLIDING_PIECES:
                get_sliding_moves()

            elif piece[1] == "K":
                get_king_moves()

    return moves


def square_has_friendly(colour: str, target_square: int, gamestate: GameState) -> bool:
    target_piece = gamestate.get_piece_on_square(target_square)
    return target_piece[0] == colour and target_piece != "--"


def square_has_enemy(colour: str, target_square: int, gamestate: GameState) -> bool:
    target_piece = gamestate.get_piece_on_square(target_square)
    return target_piece[0] != colour and target_piece != "--"


def get_pawn_moves(colour:str, square: int, gamestate: GameState) -> list[Move]:
    moves = []

    if colour == "w":

        # pushing p
        if square in range(8, 16):
            if gamestate.get_piece_on_square(square + 8) == "--":
                moves.append(Move(square, square + 8, colour + "P", "--"))
                if gamestate.get_piece_on_square(square + 16) == "--":
                    moves.append(Move(square, square + 16, colour + "P", "--"))
        if square in range(16, 56):
            if gamestate.get_piece_on_square(square + 8) == "--":
                moves.append(Move(square, square + 8, colour + "P", "--"))

        # pawn capture
        if num_squares_to_edge[square][6] > 0:
            if square_has_enemy(colour, square + 9, gamestate):
                moves.append(Move(square, square + 9, colour + "P", gamestate.get_piece_on_square(square + 9)))

        if num_squares_to_edge[square][4] > 0:
            if square_has_enemy(colour, square + 7, gamestate):
                moves.append(Move(square, square + 7, colour + "P", gamestate.get_piece_on_square(square + 7)))

    else:  # colour == "b"

        if square in range(48, 56):
            if gamestate.get_piece_on_square(square - 8) == "--":
                moves.append(Move(square, square - 8, colour + "P", "--"))
                if gamestate.get_piece_on_square(square - 16) == "--":
                    moves.append(Move(square, square - 16, colour + "P", "--"))

        if square in range(8, 48):
            if gamestate.get_piece_on_square(square - 8) == "--":
                moves.append(Move(square, square - 8, colour + "P", "--"))

        if num_squares_to_edge[square][7] > 0:
            if square_has_enemy(colour, square - 9, gamestate):
                moves.append(Move(square, square - 9, colour + "P", gamestate.get_piece_on_square(square - 9)))

        if num_squares_to_edge[square][5] > 0:
            if square_has_enemy(colour, square - 7, gamestate):
                moves.append(Move(square, square - 7, colour + "P", gamestate.get_piece_on_square(square - 7)))

    return moves


def get_knight_moves():
    pass


def get_sliding_moves():
    pass


def get_king_moves():
    pass


if __name__ == '__main__':
    print(num_squares_to_edge)