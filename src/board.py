from pieces import Egg
from move import Move


class Board:
    def __init__(self, length=5, height=6):
        self.length = length
        self.height = height
        self.grid = [[0 for _ in range(length)] for _ in range(height)]

        self.moves = []
        self.eaten_pieces = []

    def start(self):
        for cell in range(self.length):
            self.grid[0][cell] = Egg(1, [0, cell])
            self.grid[-1][cell] = Egg(2, [self.height - 1, cell])

    def apply_move(self, move: Move):
        if move.captured_pieces:
            self.eaten_pieces += move.captured_pieces
            for piece in move.captured_pieces:
                x, y = piece.position
                self.grid[x][y] = 0
        
        old_x, old_y = move.path[0]
        new_x, new_y = move.path[-1]

        move.piece.position = (new_x, new_y)
        self.grid[new_x][new_y] = move.piece
        self.grid[old_x][old_y] = 0
        

    # GETTERS

    def get_group(self, group: int):
        if group not in [1,2]:
            raise IndexError(f"No existing group {group}")
        
        return [
            piece for row in self.grid
            for piece in row
            if piece != 0 and piece.group == group
        ]   

    def __str__(self):
        s = ""
        for row in self.grid:
            s += f"{row}\n"
        return s

def main():
    ...


if __name__ == "__main__":
    main()