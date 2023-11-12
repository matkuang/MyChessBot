from board.Move import Move


class GameHistory:
    gamestates: list[str]
    moves: list[Move]

    def __init__(self):
        self.gamestates = ["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", '2kr2nr/1pbb1ppp/8/pB2N3/2Q1P3/4B3/PPP2PPP/RN2K2R b KQ - 0 1']
        self.moves = []

    def get_last_gamestate(self) -> str:
        if len(self.gamestates) > 0:
            return self.gamestates[-1]

    def pop_last_gamestate(self) -> str:
        if len(self.gamestates) > 0:
            return self.gamestates.pop()

    def save_gamestate(self, fen: str) -> None:
        self.gamestates.append(fen)

    def get_last_half_move(self) -> Move:
        if len(self.moves) > 0:
            return self.moves[-1]

    def pop_last_half_move(self) -> Move:
        if len(self.moves) > 0:
            return self.moves.pop()

    def save_half_move(self, half_move: Move) -> None:
        self.moves.append(half_move)

    def is_empty(self):
        return self.moves == []
