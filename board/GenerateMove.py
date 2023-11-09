from board.GameState import GameState
from board.Move import Move
from board.BoardUtility import num_squares_to_edge
from board.BoardUtility import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY
from board.BoardUtility import SLIDING_PIECES
from board.BoardUtility import DIRECTION_OFFSETS


def get_valid_moves(gamestate, colour_to_move) -> list[Move]:
    return get_all_moves(gamestate, colour_to_move)


def get_all_moves(gamestate: GameState, colour_to_move: str) -> list[Move]:
    moves = []
    for square in range(64):
        piece = gamestate.get_piece_on_square(square)[1]
        colour = gamestate.get_piece_on_square(square)[0]
        if colour == colour_to_move:
            if piece == PAWN:
                moves.extend(get_pawn_moves(colour, square, gamestate))
            elif piece == KNIGHT:
                get_knight_moves()

            elif piece in SLIDING_PIECES:
                moves.extend(get_sliding_moves(colour, square, gamestate))

            elif piece == KING:
                get_king_moves()

    return moves


def square_has_friendly(colour: str, target_square: int, gamestate: GameState) -> bool:
    target_piece = gamestate.get_piece_on_square(target_square)
    return target_piece[0] == colour and target_piece != EMPTY


def square_has_enemy(colour: str, target_square: int, gamestate: GameState) -> bool:
    target_piece = gamestate.get_piece_on_square(target_square)
    return target_piece[0] != colour and target_piece != EMPTY


def get_pawn_moves(colour:str, square: int, gamestate: GameState) -> list[Move]:
    moves = []

    if colour == WHITE:

        # pushing p
        if square in range(8, 16):
            if gamestate.get_piece_on_square(square + 8) == EMPTY:
                moves.append(Move(square, square + 8, colour + PAWN, EMPTY))
                if gamestate.get_piece_on_square(square + 16) == EMPTY:
                    moves.append(Move(square, square + 16, colour + PAWN, EMPTY))
        if square in range(16, 56):
            if gamestate.get_piece_on_square(square + 8) == EMPTY:
                moves.append(Move(square, square + 8, colour + PAWN, EMPTY))

        # pawn capture
        if num_squares_to_edge[square][6] > 0:
            if square_has_enemy(colour, square + 9, gamestate):
                moves.append(Move(square, square + 9, colour + PAWN, gamestate.get_piece_on_square(square + 9)))

        if num_squares_to_edge[square][4] > 0:
            if square_has_enemy(colour, square + 7, gamestate):
                moves.append(Move(square, square + 7, colour + PAWN, gamestate.get_piece_on_square(square + 7)))

    else:  # colour == BLACK

        if square in range(48, 56):
            if gamestate.get_piece_on_square(square - 8) == EMPTY:
                moves.append(Move(square, square - 8, colour + PAWN, EMPTY))
                if gamestate.get_piece_on_square(square - 16) == EMPTY:
                    moves.append(Move(square, square - 16, colour + PAWN, EMPTY))

        if square in range(8, 48):
            if gamestate.get_piece_on_square(square - 8) == EMPTY:
                moves.append(Move(square, square - 8, colour + PAWN, EMPTY))

        if num_squares_to_edge[square][7] > 0:
            if square_has_enemy(colour, square - 9, gamestate):
                moves.append(Move(square, square - 9, colour + PAWN, gamestate.get_piece_on_square(square - 9)))

        if num_squares_to_edge[square][5] > 0:
            if square_has_enemy(colour, square - 7, gamestate):
                moves.append(Move(square, square - 7, colour + PAWN, gamestate.get_piece_on_square(square - 7)))

    return moves


def get_knight_moves():
    pass


def get_sliding_moves(colour: str, square: int, gamestate: GameState):
    piece_moved = gamestate.get_piece_on_square(square)
    moves = []

    if piece_moved[1] == BISHOP:
        indices = range(4, 8)
    elif piece_moved[1] == ROOK:
        indices = range(0, 4)
    else:  # piece_moved == QUEEN:
        indices = range(0, 8)

    for direction_index in indices:
        for num in range(0, num_squares_to_edge[square][direction_index]):
            next_square = square + (num + 1) * DIRECTION_OFFSETS[direction_index]
            piece_on_next_square = gamestate.get_piece_on_square(next_square)

            if square_has_enemy(colour, next_square, gamestate):
                moves.append(Move(square, next_square, piece_moved, piece_on_next_square))
                break

            if square_has_friendly(colour, next_square, gamestate):
                break

            moves.append(Move(square, next_square, piece_moved, piece_on_next_square))

    return moves


def get_king_moves():
    pass


if __name__ == '__main__':
    pass