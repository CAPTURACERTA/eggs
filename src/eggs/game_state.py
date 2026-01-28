from eggs.board import *
from eggs.move import Move


class GameState:
    def __init__(self, board: Board):
        self.board = board
        self.turn = WHITE
        self.winner = 0

        self.moves = []

        self.temp_mandatory_moves: list[Move] = []
        self.temp_pieces_moves: dict[Egg, list[Move]] = {}

    def change_state(self, new_mandatory_moves: list[Move]):
        self.turn = self.next_player()
        self.temp_mandatory_moves = new_mandatory_moves
        self.temp_pieces_moves = {}

    def next_player(self):
        return BLACK if self.turn == WHITE else WHITE
