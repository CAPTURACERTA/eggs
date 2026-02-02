from eggs.move import Move
from eggs.types import *


class Board:
    def __init__(self, length=5, height=6):
        self.length = length
        self.height = height
        self.grid = [[EMPTY_SQUARE for _ in range(length)] for _ in range(height)]

        self.white_pieces = set()
        self.black_pieces = set()

    def apply_move(self, move: Move):
        enemy_set = self.black_pieces if move.group == WHITE else self.white_pieces
        own_set = self.white_pieces if move.group == WHITE else self.black_pieces

        if move.captured:
            for square in move.captured:
                self[square] = EMPTY_SQUARE
                enemy_set.discard(square)

        own_set.discard(move.start)
        own_set.add(move.end)

        self[move.start] = EMPTY_SQUARE
        self[move.end] = move.group

    def undo_move(self, move: Move):
        enemy_set = self.black_pieces if move.group == WHITE else self.white_pieces
        own_set = self.white_pieces if move.group == WHITE else self.black_pieces

        if move.captured:
            piece = WHITE if move.group == BLACK else BLACK
            for square in move.captured:
                self[square] = piece
                enemy_set.add(square)

        own_set.discard(move.end)
        own_set.add(move.start)

        self[move.end] = EMPTY_SQUARE
        self[move.start] = move.group

    # GETTERS

    def get_connected_group_chain(self, square: Square) -> list[Square]:
        # “Isso será reescrito quando eu otimizar.” — GPT
        chain = []
        squares_to_look = [square]
        visited = {square}

        group = self[square]

        while squares_to_look:
            current_square = squares_to_look.pop()
            chain.append(current_square)

            for peeked_square, p_square_item in self.query_square_surroundings(current_square):
                if p_square_item == group and peeked_square not in visited:
                    squares_to_look.append(peeked_square)
                    visited.add(peeked_square)

        return chain if len(chain) > 1 else []

    def get_touching_enemies(self, square: Square) -> list[Square]:     
        squares = []
        enemy_group = BLACK if self[square] == WHITE else WHITE

        for square, item_square in self.query_square_surroundings(square):
            if item_square == enemy_group:
                squares.append(square)

        return squares

    def get_group_pieces(self, group: int) -> set[Square]:
        """Returns the sets containing the pieces coordinates.\n
        So, be aware you need to make a copy of it to iterate through"""
        if group == WHITE:
            return self.white_pieces
        else:
            return self.black_pieces

    def _find_group_pieces(self, group: int) -> set[Square]:
        return {
            (x, y)
            for x, row in enumerate(self.grid)
            for y, item in enumerate(row)
            if item == group
        }

    def get_start_row(self, group: int):
        return 0 if group == WHITE else self.height - 1

    def get_goal_row(self, group: int):
        return 0 if group == BLACK else self.height - 1

    # GETTERS
    # HELPERS and ____

    def query_square_surroundings(self, square: Square):
        curr_x, curr_y = square
        offsets = ((-1, 0), (1, 0), (0, -1), (0, 1)) 

        for dx, dy in offsets:
            nx, ny = (curr_x + dx, curr_y + dy)
            if OUT_OF_BOUNDS < nx < self.height and OUT_OF_BOUNDS < ny < self.length:
                 yield (nx, ny), self.grid[nx][ny]

    def query_square(self, square: Square) -> int:
        if not self._is_within_bounds(square):
            return OUT_OF_BOUNDS

        if self[square] in [WHITE, BLACK]:
            return self[square]

        return EMPTY_SQUARE

    def _is_within_bounds(self, square: Square) -> bool:
        x, y = square
        return OUT_OF_BOUNDS < x < self.height and OUT_OF_BOUNDS < y < self.length

    def is_chained(self, piece: Square):
        for _, item in self.query_square_surroundings(piece):
            if item == self[piece]:
                return True
        return False

    def __getitem__(self, coords):
        if isinstance(coords, (list, tuple)):
            x, y = coords
            return self.grid[x][y]
        else:
            return self.grid[coords]

    def __setitem__(self, coords, value):
        x, y = coords
        self.grid[x][y] = value

    def __str__(self):
        s = ""
        for row in self.grid:
            s += f"{row}\n"

        s = s.replace("1", "⚪")
        s = s.replace("2", "⚫")
        return s

    # HELPERS and ____
    # STARTERS

    def start(self):
        for cell in range(self.length):
            self[0, cell] = WHITE
            self[-1, cell] = BLACK
        self.white_pieces = self._find_group_pieces(WHITE)
        self.black_pieces = self._find_group_pieces(BLACK)

    @ classmethod
    def custom_board(cls, grid: list[list[int]]):
        if not grid:
            raise ValueError("grid cannot be empty")
        
        height = len(grid)
        length = len(grid[0])

        for row in grid:
            if len(row) != length:
                raise ValueError("unproportional grid")
            
        board = Board(length, height)

        for col, ls in enumerate(grid):
            for line, cell in enumerate(ls):
                if cell in [WHITE, BLACK]:
                    board[col, line] = cell

        board.white_pieces = board._find_group_pieces(WHITE)
        board.black_pieces = board._find_group_pieces(BLACK)

        return board
