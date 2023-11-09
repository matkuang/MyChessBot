
WHITE, BLACK = "w", "b"
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY = "P", "N", "B", "R", "Q", "K", "--"

DIRECTION_OFFSETS = (8, -8, -1, 1, 7, -7, 9, -9)  # N S W E NW SE NE SW

SLIDING_PIECES = {BISHOP, ROOK, QUEEN}

num_squares_to_edge = []

for row in range(8):
    for col in range(8):
        num_north = 7 - row
        num_south = row
        num_west = col
        num_east = 7 - col

        num_squares_to_edge.append(
            (
                num_north,
                num_south,
                num_west,
                num_east,
                min(num_north, num_west),
                min(num_south, num_east),
                min(num_north, num_east),
                min(num_south, num_west)
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
