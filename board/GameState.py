from board.Move import Move
from board.BoardUtility import array_index_to_square, square_to_array_index
from board.BoardUtility import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY

class GameState:
    board: list[list[str]]
    moves: list[Move]
    move_made: bool
    colour_to_move: str
    white_king_square = int
    black_king_square = int
    white_can_castle = tuple[bool]
    black_can_castle = tuple[bool]

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moves = []
        self.move_made = False
        self.colour_to_move = WHITE
        self.white_king_square = 4
        self.black_king_square = 60
        self.white_can_castle = (True, True)  # king-side, queen-side
        self.black_can_castle = (True, True)

    def get_piece_on_square(self, number: int) -> str:
        index = square_to_array_index(number)
        return self.board[index[0]][index[1]]

    def make_move(self, move: Move) -> None:
        start_row = move.get_move_start_row()
        start_col = move.get_move_start_col()
        target_row = move.get_move_target_row()
        target_col = move.get_move_target_col()

        self.board[start_row][start_col] = EMPTY
        self.board[target_row][target_col] = move.piece_moved
        self.moves.append(move)
        if move.piece_moved[1] == KING:
            self.update_king_location(move.piece_moved[0])
        self.switch_turn()

    def unmake_move(self) -> None:
        if len(self.moves) > 0:
            move = self.moves.pop()

            start_row = move.get_move_start_row()
            start_col = move.get_move_start_col()
            target_row = move.get_move_target_row()
            target_col = move.get_move_target_col()

            self.board[start_row][start_col] = move.piece_moved
            self.board[target_row][target_col] = move.piece_captured
            if move.piece_moved[1] == KING:
                self.update_king_location(move.piece_moved[0])
            self.switch_turn()

    def switch_turn(self):
        if self.colour_to_move == WHITE:
            self.colour_to_move = BLACK
        else:  # self.colour_to_move == BLACK
            self.colour_to_move = WHITE

    def update_king_location(self, colour: str):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == colour + KING:
                    square = array_index_to_square((row, col))
                    if colour == WHITE:
                        self.white_king_square = square
                    else:
                        self.black_king_square = square
                    break


if __name__ == '__main__':
    gs = GameState()
    print(gs.get_piece_on_square(40))