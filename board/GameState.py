from board.Move import Move
from board.BoardUtility import array_index_to_square, square_to_array_index


class GameState:
    board: list[list[str]]
    moves: list[Move]
    move_made: bool
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
        self.move_made = False
        self.white_to_move = True

    def get_piece_on_square(self, number: int) -> str:
        index = square_to_array_index(number)
        return self.board[index[0]][index[1]]

    def make_move(self, move: Move) -> None:
        start_row = move.get_move_start_row()
        start_col = move.get_move_start_col()
        target_row = move.get_move_target_row()
        target_col = move.get_move_target_col()

        self.board[start_row][start_col] = "--"
        self.board[target_row][target_col] = move.piece_moved
        self.moves.append(move)


    def unmake_move(self) -> None:
        if len(self.moves) > 0:
            move = self.moves.pop()

            start_row = move.get_move_start_row()
            start_col = move.get_move_start_col()
            target_row = move.get_move_target_row()
            target_col = move.get_move_target_col()

            self.board[start_row][start_col] = move.piece_moved
            self.board[target_row][target_col] = move.piece_captured

            self.white_to_move = not self.white_to_move

    def switch_turn(self):
        self.white_to_move = not self.white_to_move

if __name__ == '__main__':
    gs = GameState()
    print(gs.get_piece_on_square(40))