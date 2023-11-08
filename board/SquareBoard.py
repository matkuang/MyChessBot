

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
