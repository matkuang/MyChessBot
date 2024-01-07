from board.Move import Move
from board.BoardUtility import WHITE, BLACK, EMPTY
from board.BoardUtility import array_index_to_square, square_to_array_index

piece_values = {"wP": 100, "wN": 300, "wB": 300, "wR": 500, "wQ": 900,
                "bP": -100, "bN": -300, "bB": -300, "bR": -500, "bQ": -900}


class Position:
    position: list[list[str]]

    def __init__(self, position: list[list[str]]):
        self.position = position

    def __str__(self):
        string = ""
        for row in self.position:
            for piece in row:
                string += piece + " "
            string += "\n"
        return string

    def make_move(self, move: Move) -> None:
        start_index = square_to_array_index(move.start_square)
        target_index = square_to_array_index(move.target_square)
        self.position[start_index[0]][start_index[1]] = EMPTY
        self.position[target_index[0]][target_index[1]] = move.piece_moved

    def unmake_move(self, move: Move) -> None:
        start_index = square_to_array_index(move.start_square)
        target_index = square_to_array_index(move.target_square)
        self.position[start_index[0]][start_index[1]] = move.piece_moved
        self.position[target_index[0]][target_index[1]] = move.piece_captured

    def evaluate(self) -> int:
        evaluation = 0
        evaluation += self.count_piece_values()
        return evaluation

    def count_piece_values(self) -> int:
        evaluation = 0
        for row in self.position:
            for piece in row:
                if piece in piece_values.keys():
                    evaluation += piece_values[piece]

        return evaluation


if __name__ == "__main__":

    position = Position([['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                         ['bP', '--', '--', 'bP', 'bP', 'bP', 'bP', 'bP'],
                         ['--', '--', '--', '--', '--', '--', '--', '--'],
                         ['--', '--', '--', '--', '--', '--', '--', '--'],
                         ['--', '--', '--', '--', '--', '--', '--', '--'],
                         ['--', '--', '--', '--', '--', '--', '--', '--'],
                         ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
                         ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
                        )
    position.make_move(Move(8, 16, 'wP', '--'))
    print(position)
    print(position.evaluate())