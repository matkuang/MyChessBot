from board.GameState import GameState
from board.Move import Move, Castle, EnPassant, PromotePawn
from board.BoardUtility import num_squares_to_edge
from board.BoardUtility import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY
from board.BoardUtility import SLIDING_PIECES
from board.BoardUtility import DIRECTION_OFFSETS
from board.BoardUtility import NORTH, SOUTH, WEST, EAST, NORTHWEST, SOUTHEAST, NORTHEAST, SOUTHWEST


def get_valid_moves(colour_to_move: str, gamestate: GameState) -> list[Move]:
    all_moves = get_all_moves(gamestate, colour_to_move)
    valid_moves = []

    for move in all_moves:
        gamestate.make_move(move)
        if in_check(colour_to_move, gamestate):
            pass
        else:
            valid_moves.append(move)
        gamestate.unmake_move()

    return valid_moves


def get_all_moves(gamestate: GameState, colour_to_move: str) -> list[Move]:
    moves = []
    for square in range(64):
        piece = gamestate.get_piece_on_square(square)[1]
        colour = gamestate.get_piece_on_square(square)[0]
        if colour == colour_to_move:
            if piece == PAWN:
                moves.extend(get_pawn_moves(colour, square, gamestate))
            elif piece == KNIGHT:
                moves.extend(get_knight_moves(colour, square, gamestate))

            elif piece in SLIDING_PIECES:
                moves.extend(get_sliding_moves(colour, square, gamestate))

            elif piece == KING:
                moves.extend(get_king_moves(colour, square, gamestate))

    return moves


def square_has_friendly(colour: str, target_square: int, gamestate: GameState) -> bool:
    target_piece = gamestate.get_piece_on_square(target_square)
    return target_piece[0] == colour and target_piece != EMPTY


def square_has_enemy(colour: str, target_square: int, gamestate: GameState) -> bool:
    target_piece = gamestate.get_piece_on_square(target_square)
    return target_piece[0] != colour and target_piece != EMPTY


def get_pawn_moves(colour: str, square: int, gamestate: GameState) -> list[Move]:
    moves = []

    if colour == WHITE:

        # pushing p
        if square in range(8, 16):
            if gamestate.get_piece_on_square(square + 8) == EMPTY:
                moves.append(Move(square, square + 8, colour + PAWN, EMPTY))
                if gamestate.get_piece_on_square(square + 16) == EMPTY:
                    moves.append(Move(square, square + 16, colour + PAWN, EMPTY))
        if square in range(16, 48):
            if gamestate.get_piece_on_square(square + 8) == EMPTY:
                moves.append(Move(square, square + 8, colour + PAWN, EMPTY))

        # pawn capture
        if num_squares_to_edge[square][6] > 0 and square in range(8, 48):
            if square_has_enemy(colour, square + 9, gamestate):
                moves.append(Move(square, square + 9, colour + PAWN, gamestate.get_piece_on_square(square + 9)))

        if num_squares_to_edge[square][4] > 0 and square in range(8, 48):
            if square_has_enemy(colour, square + 7, gamestate):
                moves.append(Move(square, square + 7, colour + PAWN, gamestate.get_piece_on_square(square + 7)))

        # en passant
        if gamestate.en_passant_target_square is not None:
            if square + 9 == gamestate.en_passant_target_square or square + 7 == gamestate.en_passant_target_square:
                moves.append(EnPassant(square, gamestate.en_passant_target_square, colour + PAWN, BLACK + PAWN))

        # promotion by push
        if square + 8 in range(56, 64) and gamestate.get_piece_on_square(square + 8) == EMPTY:
            for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                moves.append(PromotePawn(square, square + 8, colour + PAWN, EMPTY, colour + piece))

        # promotion by capture
        if num_squares_to_edge[square][6] > 0 and square in range(8, 48):
            if square_has_enemy(colour, square + 9, gamestate):
                enemy_piece = gamestate.get_piece_on_square(square + 9)
                for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                    moves.append(PromotePawn(square, square + 9, colour + PAWN, enemy_piece, colour + piece))

        if num_squares_to_edge[square][4] > 0 and square in range(8, 48):
            if square_has_enemy(colour, square + 7, gamestate):
                enemy_piece = gamestate.get_piece_on_square(square + 7)
                for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                    moves.append(PromotePawn(square, square + 7, colour + PAWN, enemy_piece, colour + piece))

    else:  # colour == BLACK

        if square in range(48, 56):
            if gamestate.get_piece_on_square(square - 8) == EMPTY:
                moves.append(Move(square, square - 8, colour + PAWN, EMPTY))
                if gamestate.get_piece_on_square(square - 16) == EMPTY:
                    moves.append(Move(square, square - 16, colour + PAWN, EMPTY))

        if square in range(16, 48):
            if gamestate.get_piece_on_square(square - 8) == EMPTY:
                moves.append(Move(square, square - 8, colour + PAWN, EMPTY))

        if num_squares_to_edge[square][7] > 0:
            if square_has_enemy(colour, square - 9, gamestate):
                moves.append(Move(square, square - 9, colour + PAWN, gamestate.get_piece_on_square(square - 9)))

        if num_squares_to_edge[square][5] > 0:
            if square_has_enemy(colour, square - 7, gamestate):
                moves.append(Move(square, square - 7, colour + PAWN, gamestate.get_piece_on_square(square - 7)))

        if gamestate.en_passant_target_square is not None:
            if square - 9 == gamestate.en_passant_target_square or square - 7 == gamestate.en_passant_target_square:
                moves.append(EnPassant(square, gamestate.en_passant_target_square, colour + PAWN, WHITE + PAWN))

        # promotion by push
        if square - 8 in range(0, 8) and gamestate.get_piece_on_square(square - 8) == EMPTY:
            for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                moves.append(PromotePawn(square, square - 8, colour + PAWN, EMPTY, colour + piece))

        # promotion by capture
        if num_squares_to_edge[square][7] > 0:
            if square_has_enemy(colour, square - 9, gamestate):
                enemy_piece = gamestate.get_piece_on_square(square - 9)
                for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                    moves.append(PromotePawn(square, square - 9, colour + PAWN, enemy_piece, colour + piece))

        if num_squares_to_edge[square][5] > 0:
            if square_has_enemy(colour, square - 7, gamestate):
                enemy_piece = gamestate.get_piece_on_square(square - 7)
                for piece in (KNIGHT, BISHOP, ROOK, QUEEN):
                    moves.append(PromotePawn(square, square - 7, colour + PAWN, enemy_piece, colour + piece))

    return moves


def get_knight_moves(colour: str, square: int, gamestate: GameState) -> list[Move]:
    moves = []

    if num_squares_to_edge[square][NORTH] > 0 and num_squares_to_edge[square][WEST] > 1:  # WNW
        target_square = square + 6
        moves.extend(get_knight_moves_helper(colour, gamestate, square, target_square))

    if num_squares_to_edge[square][NORTH] > 1 and num_squares_to_edge[square][WEST] > 0:  # NNW
        target_square = square + 15
        moves.extend(get_knight_moves_helper(colour, gamestate, square, target_square))

    if num_squares_to_edge[square][SOUTH] > 0 and num_squares_to_edge[square][EAST] > 1:  # ESE
        target_square = square - 6
        moves.extend(get_knight_moves_helper(colour, gamestate, square, target_square))

    if num_squares_to_edge[square][SOUTH] > 1 and num_squares_to_edge[square][EAST] > 0:  # SSE
        target_square = square - 15
        moves.extend(get_knight_moves_helper(colour, gamestate, square, target_square))

    if num_squares_to_edge[square][NORTH] > 0 and num_squares_to_edge[square][EAST] > 1:  # ENE
        target_square = square + 10
        moves.extend(get_knight_moves_helper(colour, gamestate, square, target_square))

    if num_squares_to_edge[square][NORTH] > 1 and num_squares_to_edge[square][EAST] > 0:  # NNE
        target_square = square + 17
        moves.extend(get_knight_moves_helper(colour, gamestate, square, target_square))

    if num_squares_to_edge[square][SOUTH] > 0 and num_squares_to_edge[square][WEST] > 1:  # WSW
        target_square = square - 10
        moves.extend(get_knight_moves_helper(colour, gamestate, square, target_square))

    if num_squares_to_edge[square][SOUTH] > 1 and num_squares_to_edge[square][WEST] > 0:  # SSW
        target_square = square - 17
        moves.extend(get_knight_moves_helper(colour, gamestate, square, target_square))

    return moves


def get_knight_moves_helper(colour: str, gamestate: GameState, square: int, target_square: int) -> tuple[Move]:
    piece_on_target_square = gamestate.get_piece_on_square(target_square)

    if square_has_enemy(colour, target_square, gamestate):
        return (Move(square, target_square, colour + KNIGHT, piece_on_target_square),)
    if square_has_friendly(colour, target_square, gamestate):
        return ()
    else:
        return (Move(square, target_square, colour + KNIGHT, gamestate.get_piece_on_square(target_square)),)


def get_sliding_moves(colour: str, square: int, gamestate: GameState) -> list[Move]:
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


def get_king_moves(colour: str, square: int, gamestate: GameState) -> list[Move]:
    moves = []

    for direction_index in range(0, 8):
        if num_squares_to_edge[square][direction_index] > 0:
            target_square = square + DIRECTION_OFFSETS[direction_index]
            piece_on_target_square = gamestate.get_piece_on_square(target_square)

            if square_has_enemy(colour, target_square, gamestate):
                moves.append(Move(square, target_square, colour + KING, piece_on_target_square))
                continue

            if square_has_friendly(colour, target_square, gamestate):
                continue

            moves.append(Move(square, target_square, colour + KING, piece_on_target_square))

    if check_castle_conditions(colour, KING, gamestate):
        moves.append(Castle(square, square + 2, colour + KING, EMPTY, KING))
    if check_castle_conditions(colour, QUEEN, gamestate):
        moves.append(Castle(square, square - 2, colour + KING, EMPTY, QUEEN))

    return moves


def check_castle_conditions(colour_to_castle: str, side_to_castle: str, gamestate: GameState) -> bool:
    if colour_to_castle == WHITE:
        if side_to_castle == KING:
            if not (KING in gamestate.white_castle_rights):
                return False
            if not (gamestate.get_piece_on_square(5) == EMPTY and gamestate.get_piece_on_square(6) == EMPTY):
                return False

            attacked_squares = generate_attack_map(BLACK, gamestate)
            if gamestate.white_king_square in attacked_squares or 5 in attacked_squares or 6 in attacked_squares:
                return False

            return True

        if side_to_castle == QUEEN:
            if not (QUEEN in gamestate.white_castle_rights):
                return False
            if not (all((gamestate.get_piece_on_square(square) == EMPTY) for square in range(1, 4))):
                return False

            attacked_squares = generate_attack_map(BLACK, gamestate)
            if gamestate.white_king_square in attacked_squares or any(square in attacked_squares for square in range(1, 4)):
                return False

            return True

    if colour_to_castle == BLACK:
        if side_to_castle == KING:
            if not (KING.lower() in gamestate.black_castle_rights):
                return False
            if not (gamestate.get_piece_on_square(61) == EMPTY and gamestate.get_piece_on_square(62) == EMPTY):
                return False

            attacked_squares = generate_attack_map(WHITE, gamestate)
            if gamestate.black_king_square in attacked_squares or 61 in attacked_squares or 62 in attacked_squares:
                return False

            return True

        if side_to_castle == QUEEN:
            if not (QUEEN.lower() in gamestate.black_castle_rights):
                return False
            if not (all((gamestate.get_piece_on_square(square) == EMPTY) for square in range(57, 60))):
                return False

            attacked_squares = generate_attack_map(WHITE, gamestate)
            if gamestate.black_king_square in attacked_squares or any(square in attacked_squares for square in range(57, 60)):
                return False

            return True


def get_possible_squares_for_piece(colour: str, square: int, gamestate: GameState) -> list[int]:
    possible_squares = []
    all_valid_moves = get_valid_moves(colour, gamestate)
    for move in all_valid_moves:
        if move.start_square == square:
            possible_squares.append(move.target_square)
    return possible_squares


def generate_attack_map(attack_colour: str, gamestate: GameState) -> set[int]:
    attack_squares = set()

    for square in range(64):
        piece_type = gamestate.get_piece_on_square(square)[1]
        piece_colour = gamestate.get_piece_on_square(square)[0]
        if piece_colour == attack_colour:

            if piece_type == PAWN:
                if piece_colour == WHITE:
                    if num_squares_to_edge[square][6] > 0:
                        attack_squares.add(square + 9)
                    if num_squares_to_edge[square][4] > 0:
                        attack_squares.add(square + 7)
                if piece_colour == BLACK:
                    if num_squares_to_edge[square][7] > 0:
                        attack_squares.add(square - 9)
                    if num_squares_to_edge[square][5] > 0:
                        attack_squares.add(square - 7)

            elif piece_type == KNIGHT:
                moves = get_knight_moves(piece_colour, square, gamestate)
                for move in moves:
                    attack_squares.add(move.target_square)

            elif piece_type in SLIDING_PIECES:
                moves = get_sliding_moves(piece_colour, square, gamestate)
                for move in moves:
                    attack_squares.add(move.target_square)

            elif piece_type == KING:
                for direction_index in range(0, 8):
                    if num_squares_to_edge[square][direction_index] > 0:
                        target_square = square + DIRECTION_OFFSETS[direction_index]
                        attack_squares.add(target_square)

    return attack_squares


def in_check(colour: str, gamestate: GameState) -> bool:
    if colour == WHITE:
        attack_map = generate_attack_map(BLACK, gamestate)
        return gamestate.white_king_square in attack_map
    else:
        attack_map = generate_attack_map(WHITE, gamestate)
        return gamestate.black_king_square in attack_map


if __name__ == '__main__':
    print(generate_attack_map(WHITE, GameState()))