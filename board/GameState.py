from board.Move import Move
from board.SquareBoard import array_index_to_square, square_to_array_index
class GameState:
    board: list[list]
    moves: list[Move]
    white_to_move: bool

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
        self.white_to_move = True

    def piece_on_square(self, number: int):
        index = square_to_array_index(number)
        return self.board[index[0]][index[1]]

    def make_move(self, move: Move):
        start_row = move.get_move_start_row()
        start_col = move.get_move_start_col()
        target_row = move.get_move_target_row()
        target_col = move.get_move_target_col()

        self.board[start_row][start_col] = "--"
        self.board[target_row][target_col] = move.piece_moved
        self.moves.append(move)
        self.white_to_move = not self.white_to_move

    def unmake_move(self):
        if len(self.moves) > 0:
            move = self.moves.pop()

            start_row = move.get_move_start_row()
            start_col = move.get_move_start_col()
            target_row = move.get_move_target_row()
            target_col = move.get_move_target_col()

            self.board[start_row][start_col] = move.piece_moved
            self.board[target_row][target_col] = move.piece_captured

            self.white_to_move = not self.white_to_move


if __name__ == '__main__':
    gs = GameState()
    print(gs.piece_on_square(40))