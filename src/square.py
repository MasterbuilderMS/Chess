from const import ROWS
from piece import Piece


class Square:
    def __init__(self, row, col, piece=None) -> None:
        self.row = row
        self.col = col
        self.piece: Piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece is not None

    def isempty(self):
        return not self.has_piece()

    def has_enemy_piece(self, color):
        # has piece and piece is different color
        return self.has_piece() and self.piece.color != color

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def isempty_or_enemy(self, color):
        return self.isempty() or self.has_enemy_piece(color)

    @staticmethod
    def in_range(*args):
        # all args aare within range
        for arg in args:
            if arg < 0 or arg > ROWS - 1:
                return False

        return True
