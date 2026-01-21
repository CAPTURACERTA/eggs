from copy import deepcopy
from eggs.board import Board, EMPTY_SQUARE, WHITE, BLACK
from eggs.move import Move
from eggs.pieces import Egg


class GameController:
    def __init__(self, board: Board):
        
        self.board = board
        self.group_turn = WHITE

        self.moves = []
    
        self.temp_mandatory_group_moves = self._get_group_mandatory_moves()
        self.temp_piece_legal_moves: dict[Egg, list[Move]] = {}

    def make_move(self, move: Move):
        if move.piece.group != self.group_turn:
            print("Not your turn")
            return False
        
        if move not in self.get_legal_moves(move.piece):
            print("illegal move")
            return False
        
        self.board.apply_move(move)
        self.moves.append(move)

        if self._check_win():
            self._end_game()
        else:
            self._change_turn()

        return True

    def undo_move(self):
        if not self.moves:
            print("Nada para desfazer!")
            return

        last_move = self.moves.pop()      
        self.board.undo_move(last_move)
        self._change_turn()
        

    # 
    # GET MOVES

    def iter_legal_moves_for_group(self, group):
        for piece in self.board.get_group(group):
            for move in self.get_legal_moves(piece):
                yield move


    def get_legal_moves(self, piece: Egg):
        moves = []

        if self.temp_mandatory_group_moves:
            return [
                m for m in self.temp_mandatory_group_moves if m.piece == piece
            ]

        if piece in self.temp_piece_legal_moves:
            return self.temp_piece_legal_moves[piece]
        
        if move := self._get_first_square_move(piece): moves.append(move)
        moves += self._get_basic_moves(piece, piece)
        moves += self._get_chain_moves(piece)

        self.temp_piece_legal_moves[piece] = moves

        return moves
    
    def _get_first_square_move(self, piece: Egg):
        curr_x, curr_y = piece.position
        
        home_row = self.board.get_start_row(self.group_turn)
        direction = 1 if home_row == 0 else -1

        if curr_x == home_row:
            target_x = curr_x + (2 * direction)
            final_square = (target_x, curr_y)
            intermediate_square = (target_x - direction, curr_y)

            if (self.board.query_square(intermediate_square) == EMPTY_SQUARE and
                self.board.query_square(final_square) == EMPTY_SQUARE):
                return Move(piece, [piece.position, final_square])

        return 

    def _get_basic_moves(self, query_piece: Egg, target_piece: Egg) -> list[Move | None]:
        moves = []

        curr_x, curr_y = query_piece.position

        for dx, dy in [[-1,0], [1,0], [0,-1], [0,1]]:
            square = (curr_x + dx, curr_y + dy)
            if self.board.query_square(square) == EMPTY_SQUARE:
                moves.append(Move(target_piece,[target_piece.position, square]))

        return moves

    def _get_chain_moves(self, piece: Egg):
        moves = []

        chain = self.board.get_connected_group_chain(piece)

        if chain:
            for query_piece in chain[1:]:
                moves += self._get_basic_moves(query_piece, piece)

        return moves

    def _get_group_mandatory_moves(self) -> list | list[Move]:
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
    ) -> list | list[Move]:
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

    # GET MOVES
    # HELPERS

    def _can_i_eat(self, piece: Egg, enemy: Egg):
        dx = enemy.position[0] - piece.position[0]
        dy = enemy.position[1] - piece.position[1]

        if abs(dx) + abs(dy) == 1:
            landing_square = (enemy.position[0] + dx, enemy.position[1] + dy)

            if self.board.query_square(landing_square) == EMPTY_SQUARE:
                return landing_square
        
        return ()
    
    def _can_group_move(self, group):
        return any(self.iter_legal_moves_for_group(group))

    # HELPERS
    # 

    def _change_turn(self):
        self.group_turn = BLACK if self.group_turn == WHITE else WHITE
        self.temp_mandatory_group_moves = self._get_group_mandatory_moves()
        self.temp_piece_legal_moves = {}

    def _check_win(self):   
        enemy_group = BLACK if self.group_turn == WHITE else WHITE

        if last_row_pieces := [
            piece for piece in self.board.get_group(self.group_turn)
            if piece.position[0] == self.board.get_goal_row(self.group_turn)
        ]:
            for lr_piece in last_row_pieces:
                for touching_piece in self.board.get_touching_pieces(lr_piece):
                    if self._can_i_eat(touching_piece, lr_piece):
                        break
                else:
                    return True
        elif len(self.board.get_group(enemy_group)) == 0:
            return True
        # elif not self._can_group_move(enemy_group):
        #     # problema, quando checa isso, usa o cache atual, que é do grupo atual, n do inimigo
        #     return True

        return False
    
    def _end_game(self):
        print(f"jogador {self.group_turn} vence")