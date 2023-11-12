from board.BoardUtility import square_to_array_index
from board.BoardUtility import int_to_file_rank


class Move:
    start_square: int
    target_square: int
    piece_moved: str
    piece_captured: str

    # ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    # rows_to_ranks = {ranks_to_rows[x]: x for x in ranks_to_rows}
    #
    # files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    # cols_to_files = {files_to_cols[y]: y for y in files_to_cols}

    def __init__(self, start_square: int, target_square: int, piece_moved: str, piece_captured: str):
        self.start_square = start_square
        self.target_square = target_square
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured

    def __str__(self):
        return self.get_chess_move_str()

    def __eq__(self, other):
        if isinstance(other, Move):
            return (other.start_square == self.start_square and
                    other.target_square == self.target_square and
                    other.piece_moved == self.piece_moved and
                    other.piece_captured == self.piece_captured)

    def get_chess_move_str(self) -> str:
        return int_to_file_rank[self.start_square] + int_to_file_rank[self.target_square]

    def get_move_start_row(self) -> int:
        return square_to_array_index(self.start_square)[0]

    def get_move_start_col(self) -> int:
        return square_to_array_index(self.start_square)[1]

    def get_move_target_row(self) -> int:
        return square_to_array_index(self.target_square)[0]

    def get_move_target_col(self) -> int:
        return square_to_array_index(self.target_square)[1]


class Castle(Move):
    side_to_castle: str

    def __init__(self, start_square: int, target_square: int, piece_moved: str, piece_captured: str, side_to_castle: str):
        super().__init__(start_square, target_square, piece_moved, piece_captured)
        self.side_to_castle = side_to_castle


class EnPassant(Move):
    def __init__(self, start_square: int, target_square: int, piece_moved: str, piece_captured: str):
        super().__init__(start_square, target_square, piece_moved, piece_captured)