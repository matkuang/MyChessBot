
WHITE, BLACK = "w", "b"
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY = "P", "N", "B", "R", "Q", "K", "--"

DIRECTION_OFFSETS = (8, -8, -1, 1, 7, -7, 9, -9)  # N S W E NW SE NE SW
NORTH, SOUTH, WEST, EAST, NORTHWEST, SOUTHEAST, NORTHEAST, SOUTHWEST = 0, 1, 2, 3, 4, 5, 6, 7
KNIGHT_DIRECTION_OFFSETS = (6, 15, -6, -15, 10, 17, -10, -17)  # WNW NNW ESE SSE ENE NNE WSW SSW
SLIDING_PIECES = {BISHOP, ROOK, QUEEN}

EDGE_RANK_SQUARES = (0, 1, 2, 3, 4, 5, 6, 7, 56, 57, 58, 59, 60, 61, 62, 63)

int_to_file_rank = {56: "a8", 57: "b8", 58: "c8", 59: "d8", 60: "e8", 61: "f8", 62: "g8", 63: "h8",
                    48: "a7", 49: "b7", 50: "c7", 51: "d7", 52: "e7", 53: "f7", 54: "g7", 55: "h7",
                    40: "a6", 41: "b6", 42: "c6", 43: "d6", 44: "e6", 45: "f6", 46: "g6", 47: "h6",
                    32: "a5", 33: "b5", 34: "c5", 35: "d5", 36: "e5", 37: "f5", 38: "g5", 39: "h5",
                    24: "a4", 25: "b4", 26: "c4", 27: "d4", 28: "e4", 29: "f4", 30: "g4", 31: "h4",
                    16: "a3", 17: "b3", 18: "c3", 19: "d3", 20: "e3", 21: "f3", 22: "g3", 23: "h3",
                    8: "a2", 9: "b2", 10: "c2", 11: "d2", 12: "e2", 13: "f2", 14: "g2", 15: "h2",
                    0: "a1", 1: "b1", 2: "c1", 3: "d1", 4: "e1", 5: "f1", 6: "g1", 7: "h1"}

piece_values = {"wP": 100, "wN": 300, "wB": 300, "wR": 500, "wQ": 900,
                "bP": -100, "bN": -300, "bB": -300, "bR": -500, "bQ": -900}

file_rank_to_int = {int_to_file_rank[num]: num for num in range(64)}

num_squares_to_edge = []

for row in range(8):
    for col in range(8):
        num_north = 7 - row
        num_south = row
        num_west = col
        num_east = 7 - col

        num_squares_to_edge.append(
            (
                num_north,                 # 0
                num_south,                 # 1
                num_west,                  # 2
                num_east,                  # 3
                min(num_north, num_west),  # 4
                min(num_south, num_east),  # 5
                min(num_north, num_east),  # 6
                min(num_south, num_west)   # 7
             )
        )


def array_index_to_square(index: tuple):
    return abs(56 - index[0] * 8 + index[1])


def square_to_array_index(square: int):
    """Returns the two indices (row, column) that represent the location of a square in the 2d array board
    representation.
    """
    return abs((square - 56) // 8), square % 8


if __name__ == '__main__':
    for i in range(64):
        print(square_to_array_index(i))
        print(array_index_to_square(square_to_array_index(i)))

    print(num_squares_to_edge)
    print(file_rank_to_int["a4"])
