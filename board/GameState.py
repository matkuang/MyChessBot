from board.Move import Move
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

    def makeMove(self, move: Move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.target_row][move.target_col] = move.piece_moved
        self.moves.append(move)
        self.white_to_move = not self.white_to_move
