from board.SquareBoard import array_index_to_square, square_to_array_index


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

    int_to_square = {56: "a8", 57: "b8", 58: "c8", 59: "d8", 60: "e8", 61: "f8", 62: "g8", 63: "h8",
                     48: "a7", 49: "b7", 50: "c7", 51: "d7", 52: "e7", 53: "f7", 54: "g7", 55: "h7",
                     40: "a6", 41: "b6", 42: "c6", 43: "d6", 44: "e6", 45: "f6", 46: "g6", 47: "h6",
                     32: "a5", 33: "b5", 34: "c5", 35: "d5", 36: "e5", 37: "f5", 38: "g5", 39: "h5",
                     24: "a4", 25: "b4", 26: "c4", 27: "d4", 28: "e4", 29: "f4", 30: "g4", 31: "h4",
                     16: "a3", 17: "b3", 18: "c3", 19: "d3", 20: "e3", 21: "f3", 22: "g3", 23: "h3",
                     8: "a2", 9: "b2", 10: "c2", 11: "d2", 12: "e2", 13: "f2", 14: "g2", 15: "h2",
                     0: "a1", 1: "b1", 2: "c1", 3: "d1", 4: "e1", 5: "f1", 6: "g1", 7: "h1"}

    def __init__(self, start_square: int, target_square: int, piece_moved: str, piece_captured: str):
        self.start_square = start_square
        self.target_square = target_square
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured

    def __str__(self):
        return self.get_chess_move()

    def get_chess_move(self):
        return self.int_to_square[self.start_square] + self.int_to_square[self.target_square]

    def get_move_start_row(self):
        return square_to_array_index(self.start_square)[0]

    def get_move_start_col(self):
        return square_to_array_index(self.start_square)[1]

    def get_move_target_row(self):
        return square_to_array_index(self.target_square)[0]

    def get_move_target_col(self):
        return square_to_array_index(self.target_square)[1]