import pygame as pg
from board.GameState import GameState
import assets
from board.Move import Move
from board.GenerateMove import get_valid_moves
from board.SquareBoard import array_index_to_square

colours = [(242, 226, 208), (140, 112, 95)]
board_width = board_height = 800
cell_width = cell_height = board_width // 8
cell_dimensions = (cell_width, cell_width)
images = {}


def load_images():

    pieces = ["bP", "bN", "bB", "bR", "bQ", "bK", "wP", "wN", "wB", "wR", "wQ", "wK"]
    for piece in pieces:
        images[piece] = pg.transform.smoothscale(pg.image.load(f"assets/{piece}.png"), (100, 100))


def draw_board(screen: pg.Surface):
    for file in range(8):
        for rank in range(8):
            colour = colours[(file + rank) % 2]
            coordinates = (rank * cell_width, file * cell_width)
            pg.draw.rect(screen, colour, pg.Rect(coordinates, cell_dimensions))


def draw_pieces(screen: pg.Surface, board: list[list]):
    for rank in range(8):
        for file in range(8):
            piece = board[rank][file]
            if piece != "--":
                coordinates = (file * cell_width, rank * cell_width)
                screen.blit(images[piece], pg.Rect(coordinates, cell_dimensions))


def get_target_square(screen: pg.Surface, selected_piece: tuple):
    if selected_piece is not None:
        if selected_piece[0] != "--":
            draw_dragging(screen, selected_piece)
            return int(pg.mouse.get_pos()[0] // cell_width), int(pg.mouse.get_pos()[1] // cell_width)


def draw_dragging(screen, selected_piece):
    piece, file, rank = selected_piece
    colour = colours[(file + rank) % 2]
    selected_piece_coordinates = (file * cell_width, rank * cell_width)
    pg.draw.rect(screen, colour, pg.Rect(selected_piece_coordinates, cell_dimensions))
    mouse_coordinates = (pg.mouse.get_pos()[0] - (cell_width / 2), pg.mouse.get_pos()[1] - (cell_width / 2))
    screen.blit(images[piece], mouse_coordinates)


def get_square_under_mouse(board: list[list]) -> tuple:
    location = pg.mouse.get_pos()

    file = location[0] // cell_width
    rank = location[1] // cell_width
    piece = board[rank][file]

    return piece, file, rank


def in_bounds(coordinates: tuple):
    return (board_width > coordinates[0] > 0) and (board_height > coordinates[1] > 0)


if __name__ == '__main__':

    pg.init()
    screen = pg.display.set_mode((board_width, board_height))
    load_images()
    clock = pg.time.Clock()
    gamestate = GameState()

    selected_piece = None
    drop_position = None

    valid_moves = get_valid_moves(gamestate, gamestate.white_to_move)
    move_made = False

    running = True
    while running:
        if in_bounds(pg.mouse.get_pos()):
            piece, file, rank = get_square_under_mouse(gamestate.board)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if piece != "--" and in_bounds(pg.mouse.get_pos()):
                    selected_piece = get_square_under_mouse(gamestate.board)
            if event.type == pg.MOUSEBUTTONUP:
                if drop_position is not None and in_bounds(pg.mouse.get_pos()):
                    start_square = array_index_to_square((selected_piece[2], selected_piece[1]))
                    target_square = array_index_to_square((drop_position[1], drop_position[0]))
                    piece_moved = selected_piece[0]
                    piece_captured = gamestate.piece_on_square(target_square)

                    move = Move(start_square,
                                target_square,
                                piece_moved,
                                piece_captured)
                    if move in valid_moves:
                        gamestate.make_move(move)
                        move_made = True

                selected_piece = None
                drop_position = None

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    gamestate.unmake_move()

        if move_made:
            valid_moves = get_valid_moves(gamestate, gamestate.white_to_move)

        draw_board(screen)
        draw_pieces(screen, gamestate.board)
        drop_position = get_target_square(screen, selected_piece)

        clock.tick(120)
        pg.display.flip()
