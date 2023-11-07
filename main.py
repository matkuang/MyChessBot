import time

import pygame as pg
from board.GameState import GameState
import assets

colours = [(242, 226, 208), (140, 112, 95)]
board_width = board_height = 800
cell_width = cell_height = board_width // 8
cell_dimensions = (cell_width, cell_width)
images = {}


def loadImages():

    pieces = ["bP", "bN", "bB", "bR", "bQ", "bK", "wP", "wN", "wB", "wR", "wQ", "wK"]
    for piece in pieces:
        images[piece] = pg.transform.smoothscale(pg.image.load(f"assets/{piece}.png"), (100, 100))


def drawBoard(screen: pg.Surface):
    for file in range(8):
        for rank in range(8):
            colour = colours[(file + rank) % 2]
            coordinates = (rank * cell_width, file * cell_width)
            pg.draw.rect(screen, colour, pg.Rect(coordinates, cell_dimensions))


def drawPieces(screen: pg.Surface, board: list[list]):
    for rank in range(8):
        for file in range(8):
            piece = board[rank][file]
            if piece != "--":
                coordinates = (file * cell_width, rank * cell_width)
                screen.blit(images[piece], pg.Rect(coordinates, cell_dimensions))


def drawDrag(screen: pg.Surface, selected_piece: tuple):
    if selected_piece is not None:
        piece, file, rank = selected_piece
        colour = colours[(file + rank) % 2]
        selected_piece_coordinates = (file * cell_width, rank * cell_width)
        pg.draw.rect(screen, colour, pg.Rect(selected_piece_coordinates, cell_dimensions))

        mouse_coordinates = (pg.mouse.get_pos()[0] - (cell_width / 2), pg.mouse.get_pos()[1] - (cell_width / 2))
        screen.blit(images[piece], mouse_coordinates)
        return int(pg.mouse.get_pos()[0] // cell_width), int(pg.mouse.get_pos()[1] // cell_width)


def getSquareUnderMouse(board: list[list]) -> tuple:
    location = pg.mouse.get_pos()
    file = location[0] // cell_width
    rank = location[1] // cell_width
    piece = board[rank][file]

    return piece, file, rank


if __name__ == '__main__':

    pg.init()
    screen = pg.display.set_mode((board_width, board_height))
    screen.fill((255, 255, 255))
    loadImages()
    clock = pg.time.Clock()
    gamestate = GameState()
    selected_piece = None
    drop_position = None

    running = True
    while running:
        piece, file, rank = getSquareUnderMouse(gamestate.board)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if piece != "--":
                    selected_piece = getSquareUnderMouse(gamestate.board)
            if event.type == pg.MOUSEBUTTONUP:
                if drop_position is not None:
                    piece, old_file, old_rank = selected_piece
                    gamestate.board[old_rank][old_file] = "--"
                    new_file, new_rank = drop_position
                    gamestate.board[new_rank][new_file] = piece
                selected_piece = None
                drop_position = None


        drawBoard(screen)
        drawPieces(screen, gamestate.board)
        drop_position = drawDrag(screen, selected_piece)

        clock.tick(60)
        pg.display.flip()
