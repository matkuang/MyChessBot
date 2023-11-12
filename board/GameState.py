from board.Move import Move, Castle
from board.BoardUtility import array_index_to_square, square_to_array_index, int_to_file_rank, file_rank_to_int
from board.BoardUtility import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY
from board.GameHistory import GameHistory


class GameState:
    game_history = GameHistory
    board: list[list[str]]
    moves: list[Move]
    colour_to_move: str
    white_king_square = int
    black_king_square = int
    white_castle_rights = list[str]
    black_castle_rights = list[str]
    old_white_castle_rights = tuple[bool]
    old_black_castle_rights = tuple[bool]
    en_passant_target_square: int | None
    half_move_clock: int
    full_move_number: int

    def __init__(self, fen: str, game_history: GameHistory):
        # self.board = [
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        #     ["wR", "--", "--", "--", "wK", "wB", "wN", "wR"]
        # ]
        # self.moves = []
        # self.move_made = False
        # self.colour_to_move = WHITE
        # self.white_king_square = 4
        # self.black_king_square = 60
        # self.white_castle_rights = [KING, QUEEN]  # king-side, queen-side
        # self.black_castle_rights = [KING.lower(), QUEEN.lower()]
        # self.en_passant_target_square = None
        # self.half_move_clock = 0
        # self.full_move_number = 1

        self.load_gamestate_from_fen(fen, game_history)

    def load_gamestate_from_fen(self, fen: str, game_history: GameHistory):
        colours = (WHITE, BLACK)
        fen_list = fen.split(" ")
        board_fen_as_list = fen_list[0].split("/")
        self.game_history = game_history
        self.colour_to_move = fen_list[1]
        self.white_castle_rights = [character for character in fen_list[2] if character.isupper()]
        self.black_castle_rights = [character for character in fen_list[2] if character.islower()]
        if fen_list[3] != "-":
            self.en_passant_target_square = file_rank_to_int[fen_list[3]]
        else:
            self.en_passant_target_square = None
        self.half_move_clock = int(fen_list[4])
        self.full_move_number = int(fen_list[5])
        board = []
        white_king_tracker_row, white_king_tracker_col = -1, -1
        black_king_tracker_row, black_king_tracker_col = -1, -1
        for row_string in board_fen_as_list:
            row = []
            for character in row_string:
                if character.isnumeric():
                    for num in range(int(character)):
                        row.append(EMPTY)
                        white_king_tracker_col += 1
                        black_king_tracker_col += 1
                else:
                    colour = colours[character.islower()]
                    row.append(colour + character.upper())
                    white_king_tracker_col += 1
                    black_king_tracker_col += 1

                if character == KING.upper():
                    self.white_king_square = array_index_to_square((white_king_tracker_row, white_king_tracker_col))
                if character == KING.lower():
                    self.black_king_square = array_index_to_square((black_king_tracker_row, black_king_tracker_col))

                white_king_tracker_row += 1
                black_king_tracker_row += 1

            board.append(row)
        self.board = board

    def __str__(self):
        string = ""
        for row in self.board:
            for col in row:
                string += col + " "
            string += "\n"
        return string

    def generate_fen(self):
        fen_string = ""

        for row in self.board:
            empty_squares = 0
            for piece in row:
                if piece == EMPTY:
                    empty_squares += 1
                    continue
                else:
                    if piece[0] == BLACK:
                        fen_piece = piece[1].lower()
                    else:
                        fen_piece = piece[1]

                    fen_string += str(empty_squares) + fen_piece
                    empty_squares = 0

            fen_string += str(empty_squares) + "/"
        fen_string = fen_string.replace("0", "")
        fen_string = fen_string[0:-1] + " " + self.colour_to_move + " "

        if self.white_castle_rights == [] and self.black_castle_rights == []:
            fen_string += "-" + " "
        else:
            castle_rights = self.white_castle_rights + self.black_castle_rights
            castle_rights_string = "".join(sorted(castle_rights))

            fen_string += castle_rights_string + " "

        if self.en_passant_target_square is None:
            fen_string += "-" + " "
        else:
            fen_string += int_to_file_rank[self.en_passant_target_square] + " "

        fen_string += f"{self.half_move_clock} {self.full_move_number}"

        return fen_string

    def get_piece_on_square(self, square: int) -> str:
        index = square_to_array_index(square)
        return self.board[index[0]][index[1]]

    def set_piece_on_square(self, square: int, piece: str) -> None:
        index = square_to_array_index(square)
        target_row, target_col = index[0], index[1]
        self.board[target_row][target_col] = piece

    def make_move(self, move: Move) -> None:

        piece_type = move.piece_moved[1]
        piece_colour = move.piece_moved[0]

        # Updates the game board by moving piece moved
        self.set_piece_on_square(move.start_square, EMPTY)
        self.set_piece_on_square(move.target_square, move.piece_moved)

        # Updates the game board by moving the ROOK if move was castling move
        if piece_type == KING:
            self.update_king_location(piece_colour)
            rook_square_king = move.start_square + 3
            rook_square_queen = move.start_square - 4

            if move.target_square - move.start_square == 2:  # king-side castle
                self.set_piece_on_square(rook_square_king, EMPTY)
                self.set_piece_on_square(rook_square_king - 2, piece_colour + ROOK)
            if move.target_square - move.start_square == -2:  # queen-side castle
                self.set_piece_on_square(rook_square_queen, EMPTY)
                self.set_piece_on_square(rook_square_queen + 3, piece_colour + ROOK)

            self.lose_castle_rights(piece_colour, KING)
            self.lose_castle_rights(piece_colour, QUEEN)

            if (self.white_castle_rights != []) or (self.black_castle_rights != []):
                self.lose_castle_rights(piece_colour, KING)
                self.lose_castle_rights(piece_colour, QUEEN)

        # Losing castling rights accordingly if KING or ROOK is moved from original square

        if piece_type == ROOK and ((self.white_castle_rights != []) or (self.black_castle_rights != [])):
            if piece_colour == WHITE:
                if self.get_piece_on_square(7) == EMPTY:
                    self.lose_castle_rights(WHITE, KING)
                elif self.get_piece_on_square(0) == EMPTY:
                    self.lose_castle_rights(WHITE, QUEEN)
            else:
                if self.get_piece_on_square(63) == EMPTY:
                    self.lose_castle_rights(BLACK, KING)
                elif self.get_piece_on_square(56) == EMPTY:
                    self.lose_castle_rights(BLACK, QUEEN)

        self.game_history.save_half_move(move)
        self.switch_turn()
        self.game_history.save_gamestate(self.generate_fen())

    def unmake_move(self) -> None:
        # if not self.game_history.is_empty():
        #     move = self.moves.pop()
        #     piece_type = move.piece_moved[1]
        #     piece_colour = move.piece_moved[0]
        #     self.set_piece_on_square(move.start_square, move.piece_moved)
        #     self.set_piece_on_square(move.target_square, move.piece_captured)
        #
        #     if isinstance(move, Castle):
        #         rook_square_king = move.start_square + 3
        #         rook_square_queen = move.start_square - 4
        #         if move.side_to_castle == KING:
        #             self.set_piece_on_square(rook_square_king, piece_colour + ROOK)
        #             self.set_piece_on_square(rook_square_king - 2, EMPTY)
        #         else:  # move.side_to_castle == QUEEN
        #             self.set_piece_on_square(rook_square_queen, piece_colour + ROOK)
        #             self.set_piece_on_square(rook_square_queen + 3, EMPTY)
        #
        #
        #     if piece_type == KING:
        #         self.update_king_location(move.piece_moved[0])
        #
        #     self.switch_turn()
        if not self.game_history.is_empty():
            self.game_history.pop_last_half_move()  # don't know what to do with this for now
            self.game_history.pop_last_gamestate()  # removes the current gamestate since the one we want is in index -2
            self.load_gamestate_from_fen(self.game_history.get_last_gamestate(), self.game_history)

    def switch_turn(self) -> None:
        if self.colour_to_move == WHITE:
            self.colour_to_move = BLACK
        else:  # self.colour_to_move == BLACK
            self.colour_to_move = WHITE

    def update_king_location(self, colour: str) -> None:
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == colour + KING:
                    square = array_index_to_square((row, col))
                    if colour == WHITE:
                        self.white_king_square = square
                    else:
                        self.black_king_square = square
                    break

    def lose_castle_rights(self, colour: str, side_to_castle: str) -> None:
        if colour == WHITE:
            if side_to_castle in self.white_castle_rights:
                self.white_castle_rights.remove(side_to_castle)

        if colour == BLACK:
            if side_to_castle.lower() in self.black_castle_rights:
                self.black_castle_rights.remove(side_to_castle.lower())

    def get_colour_to_move(self):
        return self.colour_to_move


if __name__ == '__main__':
    gs = GameState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", GameHistory())
    print(gs)
    print(gs.generate_fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")