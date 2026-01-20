from pieces import Egg
from move import Move


OUT_OF_BOUNDS = -1
EMPTY_SQUARE = 0
WHITE = 1
BLACK = 2

class Board:
    def __init__(self, length=5, height=6):
        self.length = length
        self.height = height
        self.grid = [[EMPTY_SQUARE for _ in range(length)] for _ in range(height)]


    def start(self):
        for cell in range(self.length):
            self[0, cell] = Egg(WHITE, (0, cell))
            self[-1, cell] = Egg(BLACK, (self.height - 1, cell))

    def apply_move(self, move: Move):
        if move.captured_pieces:
            for piece in move.captured_pieces:
                self[piece.position] = EMPTY_SQUARE
        
        old_x, old_y = move.path[0]
        new_x, new_y = move.path[-1]

        move.piece.position = (new_x, new_y)
        self[new_x, new_y] = move.piece
        self[old_x, old_y] = EMPTY_SQUARE

    def undo_move(self, move: Move):
        if move.captured_pieces:
            for piece in move.captured_pieces:
                self[piece.position] = piece
        
        old_x, old_y = move.path[-1]
        new_x, new_y = move.path[0]

        move.piece.position = (new_x, new_y)
        self[new_x, new_y] = move.piece
        self[old_x, old_y] = EMPTY_SQUARE

    # GETTERS

    def get_connected_group_chain(self, piece: Egg) -> list[Egg]:
        chain = []
        pieces_to_look = [piece]
        visited = {piece}

        while pieces_to_look:
            current_piece = pieces_to_look.pop()
            chain.append(current_piece)   
            
            for square, item_square in self.query_piece_surroundings(current_piece):
                if (item_square == piece.group and 
                    self[square] not in visited):
                    pieces_to_look.append(self[square])
                    visited.add(self[square])

        return chain if len(chain) > 1 else []

    def get_group(self, group: int) -> list[Egg]:
        if group not in [1,2]:
            raise IndexError(f"No existing group {group}")
        
        return [
            piece for row in self.grid
            for piece in row
            if piece != EMPTY_SQUARE and piece.group == group
        ]   

    def get_touching_pieces(self, piece: Egg) -> tuple[Egg, ...]:
        touching_pieces = []
        enemy_group = BLACK if piece.group == WHITE else WHITE

        for square, item_square in self.query_piece_surroundings(piece):
            if item_square == enemy_group:
                touching_pieces.append(self[square])

        return tuple(touching_pieces) 

    def get_start_row(self, group: int):
        return 0 if group == WHITE else self.height - 1
    
    def get_goal_row(self, group: int):
        return 0 if group == BLACK else self.height - 1

    # HELPERS and ____

    def query_piece_surroundings(self, piece: Egg) -> list[tuple[tuple[int, int], int]]:
        surrounds = []

        curr_x, curr_y = piece.position

        for dx, dy in [[-1,0], [1,0], [0,-1], [0,1]]:
            square = curr_x + dx, curr_y + dy
            item_square = self.query_square(square)

            if item_square != OUT_OF_BOUNDS: 
                surrounds.append(
                    (square, item_square)
                )

        return surrounds

    def query_square(self, square: tuple[int, int]) -> int:
        if not self._is_within_bounds(square):
            return OUT_OF_BOUNDS 
        
        if isinstance(self[square], Egg):
            return self[square].group
            
        return EMPTY_SQUARE

    def _is_within_bounds(self, pos: tuple[int, int]) -> bool:
        x, y = pos
        return (OUT_OF_BOUNDS < x < self.height and 
                OUT_OF_BOUNDS < y < self.length)

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
        return s