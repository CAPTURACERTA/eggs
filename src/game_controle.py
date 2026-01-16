from copy import deepcopy
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
        moves = []

        if self.mandatory_group_moves:
            for move in self.mandatory_group_moves:
                if piece == move.piece:
                    moves.append(move)
        else:
            if move := self._get_first_square_move(piece): moves.append(move)
            moves += self._get_basic_moves(piece, piece)
            moves += self._get_chain_moves(piece)

        return moves
    
    def _get_first_square_move(self, piece: Egg):
        curr_x, curr_y = piece.position
        
        start_row = 0 if piece.group == 1 else self.board.height - 1
        direction = 1 if start_row == 0 else -1

        if curr_x == start_row:
            target_x = curr_x + (2 * direction)
            final_square = (target_x, curr_y)
            intermediate_square = (target_x - direction, curr_y)

            if (self.board.query_square(intermediate_square) == 0 and
                self.board.query_square(final_square) == 0):
                return Move(piece, [piece.position, final_square])

        return 


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

    def _get_group_mandatory_moves(self):
        moves = []

        for piece in self.board.get_group(self.group_turn):
            moves += self._get_mandatory_moves(piece)

        return [
            move for move in moves if len(move.captured_pieces) == max(
                [len(m.captured_pieces) for m in moves]
            )
        ]
    
    def _get_mandatory_moves(
        self, piece: Egg, current_move: Move = None
    ):
        moves = []

        if current_move is None:
            current_move = Move(piece, [piece.position])

        found_continuation = False

        for enemy in self.board.get_touching_pieces(piece):
            if landing_square := self._can_i_eat(piece, enemy):
                found_continuation = True

                temp_move = Move(piece, [piece.position, landing_square], [enemy,])
                current_move.path.append(landing_square)
                current_move.captured_pieces.append(enemy)

                self.board.apply_move(temp_move)
                moves += self._get_mandatory_moves(piece, current_move)

                self.board.undo_move(temp_move)
                current_move.path.pop()
                current_move.captured_pieces.pop()
        if (not found_continuation and 
            len(current_move.captured_pieces) > 0):
            moves.append(deepcopy(current_move))

        return moves

    def _can_i_eat(self, piece: Egg, enemy: Egg):
        dx = enemy.position[0] - piece.position[0]
        dy = enemy.position[1] - piece.position[1]

        if abs(dx) + abs(dy) == 1:
            landing_square = (enemy.position[0] + dx, enemy.position[1] + dy)

            if self.board.query_square(landing_square) == 0:
                return landing_square
        
        return ()
    
    # preciso aplicar a lógica no get_basic_moves para não permitir, pois há movimentos obrigatórios