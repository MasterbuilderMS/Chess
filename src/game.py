import pygame
from const import ROWS, COLS, SQSIZE, HEIGHT
from board import Board
from dragger import Dragger
from piece import Piece
from config import Config
from square import Square


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.dragger = Dragger()
        self.current_player = "white"  # white starts
        self.hovered_sqr = None
        self.config = Config()

    # show methods

    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    label = self.config.font.render(str(ROWS - row), True, color)
                    label_pos = (5, 5 + row * SQSIZE)
                    surface.blit(label, label_pos)

                # row coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if col % 2 == 1 else theme.bg.light
                    # label
                    label = self.config.font.render(
                        Square.get_alphacol(col), True, color
                    )
                    label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(label, label_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = (
                            col * SQSIZE + SQSIZE // 2,
                            row * SQSIZE + SQSIZE // 2,
                        )
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece: Piece = self.dragger.piece
            # loop all values
            for move in piece.moves:
                # color
                color = (
                    theme.moves.light
                    if (move.final.row + move.final.col) % 2 == 0
                    else theme.moves.dark
                )
                # create a rect
                rect = (
                    move.final.col * SQSIZE,
                    move.final.row * SQSIZE,
                    SQSIZE,
                    SQSIZE,
                )
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move is not None:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                # color
                color = (
                    theme.trace.light
                    if (pos.row + pos.col) % 2 == 0
                    else theme.trace.light
                )
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr is not None:
            color = (180, 180, 180)
            rect = (
                self.hovered_sqr.col * SQSIZE,
                self.hovered_sqr.row * SQSIZE,
                SQSIZE,
                SQSIZE,
            )
            pygame.draw.rect(surface, color, rect, width=5)

    # other methods
    def next_player(self):
        self.current_player = "black" if self.current_player == "white" else "white"

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, capture=False):
        if capture:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
