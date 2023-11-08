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
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.target_row][move.target_col] = move.piece_moved
        self.moves.append(move)
        self.white_to_move = not self.white_to_move

    def unmake_move(self):
        if len(self.moves) > 0:
            move = self.moves.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.target_row][move.target_col] = move.piece_captured


if __name__ == '__main__':
    gs = GameState()
    print(gs.piece_on_square(40))