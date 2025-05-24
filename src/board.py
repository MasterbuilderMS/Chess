from const import COLS, ROWS
from square import Square
from piece import Pawn, Knight, Bishop, Rook, King, Queen, Piece
from move import Move


class Board:
    def __init__(self):
        self.squares = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    def move(self, piece: Piece, move: Move):
        initial = move.initial
        final = move.final

        # update console board
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        piece.moved = True
        # clear valid moves
        piece.clear_moves()
        self.last_move = move

    def valid_move(self, piece: Piece, move):
        return move in piece.moves

    def calc_moves(self, piece: Piece, row, col):
        """
        Calculates all the possible (valid) moves that a given piece can make,
        on a specific position
        """

        def pawn_moves():
            # number of steps the pawn can move
            steps = 1 if piece.moved else 2
            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)
                        piece.add_moves(move)
                    else:
                        # if first square is full, still cant go to second
                        break
                else:
                    break

            # diagonal moves
            possible_move_row = row + piece.dir  # advance one step up or down the board
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][
                        possible_move_col
                    ].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a new move
                        move = Move(initial, final)
                        piece.add_moves(move)

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][
                        possible_move_col
                    ].isempty_or_enemy(piece.color):
                        # create new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_moves(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece  # fmt: off
                        final = Square(
                            possible_move_row, possible_move_col, final_piece
                        )
                        move = Move(initial, final)
                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # create new move
                            piece.add_moves(move)
                        # has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):  # fmt: off
                            # create new move
                            piece.add_moves(move)
                            break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):  # fmt: off
                            break
                    else:
                        break
                    # step further
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            possible_moves = [
                (row - 1, col + 0),  # up
                (row - 1, col + 1),  # up-right
                (row + 0, col + 1),  # right
                (row + 1, col + 1),  # down-right
                (row + 1, col + 0),  # down
                (row + 1, col - 1),  # down-left
                (row + 0, col - 1),  # left
                (row - 1, col - 1),  # up-left
            ]
            for move in possible_moves:
                pos_row, pos_col = move
                if Square.in_range(pos_row, pos_col):
                    if self.squares[pos_row][pos_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(pos_row, pos_col)
                        move = Move(initial, final)
                        piece.add_moves(move)

            # TODO: castling

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves(
                [
                    (1, 1),  # down-right
                    (-1, -1),  # up-left
                    (-1, 1),  # up-right
                    (1, -1),  # down-left
                ]
            )
        elif isinstance(piece, Rook):
            straightline_moves(
                [
                    (-1, 0),  # up
                    (0, 1),  # right
                    (1, 0),  # down
                    (0, -1),  # left
                ]
            )
        elif isinstance(piece, Queen):
            straightline_moves(
                [
                    (-1, 0),  # up
                    (0, 1),  # right
                    (1, 0),  # down
                    (0, -1),  # left
                    (1, 1),  # down-right
                    (-1, -1),  # up-left
                    (-1, 1),  # up-right
                    (1, -1),  # down-left
                ]
            )
        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)
        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        # debugging: self.squares[5][0] = Square(5, 0, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # king
        self.squares[row_other][4] = Square(row_other, 3, King(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 4, Queen(color))
