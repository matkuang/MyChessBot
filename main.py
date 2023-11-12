import pygame as pg
from board.GameState import GameState
from board.GameHistory import GameHistory
import assets
from board.Move import Move
from board.GenerateMove import get_valid_moves, get_possible_squares_for_piece, in_check
from board.BoardUtility import array_index_to_square, square_to_array_index
from board.BoardUtility import WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY

colours = [(242, 226, 208), (140, 112, 95)]
highlight_colours = [(232, 128, 138), (230, 101, 113)]  # light, dark

board_width = board_height = 800
cell_width = cell_height = board_width // 8
cell_dimensions = (cell_width, cell_width)
images = {}


def load_images():

    pieces = ["bP", "bN", "bB", "bR", "bQ", "bK", "wP", "wN", "wB", "wR", "wQ", "wK"]
    for piece in pieces:
        images[piece] = pg.transform.smoothscale(pg.image.load(f"assets/{piece}.png"), (100, 100))
    images["WIN"] = pg.transform.smoothscale(pg.image.load("assets/WIN.png"), (400, 400))
    images["LOSE"] = pg.transform.smoothscale(pg.image.load("assets/LOSE.png"), (400, 400))
    images["DRAW"] = pg.transform.smoothscale(pg.image.load("assets/DRAW.png"), (400, 400))


def draw_board(screen: pg.Surface, selected_piece: tuple):
    for file in range(8):
        for rank in range(8):
            colour = colours[(file + rank) % 2]
            coordinates = (rank * cell_width, file * cell_width)
            pg.draw.rect(screen, colour, pg.Rect(coordinates, cell_dimensions))

    if selected_piece is not None:
        start_square = array_index_to_square((selected_piece[2], selected_piece[1]))
        piece_colour = selected_piece[0][0]
        possible_squares = get_possible_squares_for_piece(piece_colour, start_square, gamestate)

        for square in possible_squares:
            array_index = square_to_array_index(square)
            highlight_colour = highlight_colours[(array_index[0] + array_index[1]) % 2]
            highlight_square(screen, square, gamestate.get_piece_on_square(square), highlight_colour)


def draw_pieces(screen: pg.Surface, gamestate: GameState):
    row_num = 0
    for row in gamestate.board:
        col_num = 0
        for piece in row:
            if piece != EMPTY:
                coordinates = (col_num * cell_width, row_num * cell_height)
                screen.blit(images[piece], pg.Rect(coordinates, cell_dimensions))
            col_num += 1
        row_num += 1


def get_target_square(screen: pg.Surface, selected_piece: tuple):
    if selected_piece is not None:
        if selected_piece[0] != EMPTY:
            draw_dragging(screen, selected_piece)
            return int(pg.mouse.get_pos()[0] // cell_width), int(pg.mouse.get_pos()[1] // cell_height)


def draw_dragging(screen, selected_piece):
    piece, file, rank = selected_piece
    colour = colours[(file + rank) % 2]
    highlight_colour = (227, 61, 77)
    selected_piece_coordinates = (file * cell_width, rank * cell_height)
    pg.draw.rect(screen, colour, pg.Rect(selected_piece_coordinates, cell_dimensions))
    selected_square = array_index_to_square((selected_piece[2], selected_piece[1]))
    highlight_square(screen, selected_square, "--", highlight_colour)
    mouse_coordinates = (pg.mouse.get_pos()[0] - (cell_width / 2), pg.mouse.get_pos()[1] - (cell_height / 2))
    screen.blit(images[piece], mouse_coordinates)


def get_square_under_mouse(board: list[list]) -> tuple:
    location = pg.mouse.get_pos()

    file = location[0] // cell_width
    rank = location[1] // cell_width
    piece = board[rank][file]

    return piece, file, rank


def in_bounds(coordinates: tuple):
    return (board_width > coordinates[0] > 0) and (board_height > coordinates[1] > 0)


def highlight_square(screen: pg.Surface, square: int, piece: str, highlight_colour: tuple):
    array_index = square_to_array_index(square)
    square_coordinates = (array_index[1] * cell_width, array_index[0] * cell_height)
    pg.draw.rect(screen, highlight_colour, pg.Rect(square_coordinates, cell_dimensions))
    if piece != "--":
        screen.blit(images[piece], square_coordinates)


def draw_end_screen(screen: pg.Surface, winning_colour: str | None, gamestate: GameState):
    if winning_colour == WHITE:
        draw_board(screen, selected_piece)
        draw_pieces(screen, gamestate)
        screen.blit(images["WIN"], pg.Rect((200, 200), (400, 400)))
    elif winning_colour == BLACK:
        draw_board(screen, selected_piece)
        draw_pieces(screen, gamestate)
        screen.blit(images["LOSE"], pg.Rect((200, 200), (400, 400)))
    else:
        draw_board(screen, selected_piece)
        draw_pieces(screen, gamestate)
        screen.blit(images["DRAW"], pg.Rect((200, 200), (400, 400)))


if __name__ == '__main__':

    pg.init()
    screen = pg.display.set_mode((board_width, board_height))
    load_images()
    clock = pg.time.Clock()
    game_history = GameHistory()
    gamestate = GameState("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", game_history)

    selected_piece = None
    drop_position = None

    valid_moves = get_valid_moves(gamestate.colour_to_move, gamestate)
    move_made = False

    running = True
    while running:

        if valid_moves == []:
            draw_board(screen, selected_piece)
            draw_pieces(screen, gamestate)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            if gamestate.colour_to_move == BLACK:
                if in_check(BLACK, gamestate):  # white wins by checkmate
                    draw_end_screen(screen, WHITE, gamestate)
                else:
                    draw_end_screen(screen, None, gamestate)  # draw by stalemate

            if gamestate.colour_to_move == WHITE:
                if in_check(WHITE, gamestate):  # black wins by checkmate
                    draw_end_screen(screen, BLACK, gamestate)
                else:
                    draw_end_screen(screen, None, gamestate)  # draw by stalemate

            pg.display.flip()

        else:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    if selected_piece is None:
                        if in_bounds(pg.mouse.get_pos()):
                            piece, file, rank = get_square_under_mouse(gamestate.board)
                            if piece != EMPTY and in_bounds(pg.mouse.get_pos()):
                                selected_piece = get_square_under_mouse(gamestate.board)

                if event.type == pg.MOUSEBUTTONUP:
                    if drop_position is not None and in_bounds(pg.mouse.get_pos()):
                        start_square = array_index_to_square((selected_piece[2], selected_piece[1]))
                        target_square = array_index_to_square((drop_position[1], drop_position[0]))
                        piece_moved = selected_piece[0]
                        piece_captured = gamestate.get_piece_on_square(target_square)

                        for valid_move in valid_moves:
                            if valid_move.start_square == start_square and valid_move.target_square == target_square:
                                gamestate.make_move(valid_move)
                                move_made = True
                                if valid_move.piece_moved[1] == KING:
                                    gamestate.update_king_location(gamestate.get_colour_to_move())
                                break

                    selected_piece = None
                    drop_position = None

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_z:
                        gamestate.unmake_move()
                        valid_moves = get_valid_moves(gamestate.colour_to_move, gamestate)
                    if event.key == pg.K_s:
                        print(gamestate.generate_fen())

                if move_made:
                    move_made = False
                    valid_moves = get_valid_moves(gamestate.colour_to_move, gamestate)

            draw_board(screen, selected_piece)
            draw_pieces(screen, gamestate)
            drop_position = get_target_square(screen, selected_piece)

            clock.tick(120)
            pg.display.flip()
