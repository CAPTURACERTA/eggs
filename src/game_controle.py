from board import Board
from move import Move
from pieces import Egg


class GameControler:
    def __init__(self, board: Board):
        
        self.board = board
        self.group_turn = 1
        self.mandatory_group_moves: list[Move] = []

        self.moves = []
    

    def get_legal_moves(self, piece: Egg):
        if self.mandatory_group_moves:
            for move in self.mandatory_group_moves:
                if piece == move.piece:
                    return move
            return None
        
        moves = []

        if move := self._get_first_square_move(piece): moves.append(move)
        moves += self._get_basic_moves(piece, piece)
        moves += self._get_chain_moves(piece)

        return moves
    
    def _get_first_square_move(self, piece: Egg):
        move = None
        curr_x, curr_y = piece.position
        
        if piece.group == 1:
            start_row = 0
            direction = 1 
        else: 
            start_row = self.board.height - 1
            direction = -1 

        if curr_x == start_row:
            target_x = curr_x + (2 * direction)
            final_square = (target_x, curr_y)
            intermediate_square = (direction, curr_y)

            if (self.board.query_square(intermediate_square) == 0 and
                self.board.query_square(final_square) == 0):
                move = Move(piece, [piece.position, final_square])

        return move


    def _get_basic_moves(self, query_piece: Egg, target_piece: Egg) -> list[Move | None]:
        moves = []

        curr_x, curr_y = query_piece.position

        for dx, dy in [[-1,0], [1,0], [0,-1], [0,1]]:
            square = (curr_x + dx, curr_y + dy)
            if self.board.query_square(square) == 0:
                moves.append(Move(target_piece,[target_piece.position, square]))

        return moves

    def _get_chain_moves(self, piece: Egg):
        moves = []

        chain = self.board.get_chain(piece)

        if chain:
            for query_piece in chain[1:]:
                moves += self._get_basic_moves(query_piece, piece)

        return moves


    def _search_group_mandatory_moves(self):
        ...