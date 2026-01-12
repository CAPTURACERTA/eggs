from board import Board
from pieces import Egg


class GameControler:
    def __init__(self, board: Board):
        
        self.board = board
        self.group_turn = 1

    
    def move_piece(self, piece: Egg, position: tuple[int, int]):
        if piece.get_group() != self.group_turn:
            print("Not your turn")
            return

        self.board.move_piece(piece, position)