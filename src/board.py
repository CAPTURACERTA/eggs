from pieces import Egg
from move import Move


class Board:
    def __init__(self, length=5, height=6):
        self.length = length
        self.height = height
        self.grid = [[0 for _ in range(length)] for _ in range(height)]


    def start(self):
        for cell in range(self.length):
            self[0, cell] = Egg(1, (0, cell))
            self[-1, cell] = Egg(2, (self.height - 1, cell))

    def apply_move(self, move: Move):
        if move.captured_pieces:
            for piece in move.captured_pieces:
                self[piece.position] = 0
        
        old_x, old_y = move.path[0]
        new_x, new_y = move.path[-1]

        move.piece.position = (new_x, new_y)
        self[new_x, new_y] = move.piece
        self[old_x, old_y] = 0

    def undo_move(self, move: Move):
        if move.captured_pieces:
            for piece in move.captured_pieces:
                self[piece.position] = piece
        
        old_x, old_y = move.path[-1]
        new_x, new_y = move.path[0]

        move.piece.position = (new_x, new_y)
        self[new_x, new_y] = move.piece
        self[old_x, old_y] = 0

    # GETTERS

    def get_chain(self, piece: Egg) -> list[Egg]:
        chain = []
        pieces_to_look = [piece]
        visited = {piece}

        while pieces_to_look:
            current_piece = pieces_to_look.pop()
            chain.append(current_piece)   
            
            for square, item_square in self.query_piece_surrounds(current_piece):
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
            if piece != 0 and piece.get_group() == group
        ]   

    def get_touching_pieces(self, piece: Egg) -> tuple[Egg, ...]:
        touching_pieces = []
        enemy_group = 2 if piece.group == 1 else 1

        for square, item_square in self.query_piece_surrounds(piece):
            if item_square == enemy_group:
                touching_pieces.append(self[square])

        return tuple(touching_pieces) 



    # HELPERS and ____

    def query_piece_surrounds(self, piece: Egg) -> list[tuple[tuple[int, int], int]]:
        surrounds = []

        curr_x, curr_y = piece.position

        for dx, dy in [[-1,0], [1,0], [0,-1], [0,1]]:
            square = curr_x + dx, curr_y + dy
            item_square = self.query_square(square)

            if item_square != -1: 
                surrounds.append(
                    (square, item_square)
                )

        return surrounds

    def query_square(self, square: tuple[int, int]) -> int:
        x, y = square

        if not self._is_within_bounds(x, y):
            return -1 
        
        item = self[x, y] 
        if isinstance(item, Egg):
            return item.get_group()
        return 0

    def _is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.length

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

def main():
    ...


if __name__ == "__main__":
    main()