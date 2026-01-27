from eggs.game_state import GameState
from eggs.board import *
from eggs.pieces import Egg
from eggs.move import Move
from copy import deepcopy


class GameRules:
    # MOVES GETTERS

    @staticmethod
    def get_piece_legal_moves(state: GameState, piece: Egg):
        moves = []

        if move := GameRules._get_first_square_move(state, piece):
            moves.append(move)
        moves += GameRules._get_piece_basic_moves(state, piece, piece)
        moves += GameRules._get_chain_moves(state, piece)

        return moves

    @staticmethod
    def _get_first_square_move(state: GameState, piece: Egg):
        curr_x, curr_y = piece.position

        start_row = state.board.get_start_row(piece.group)
        direction = 1 if start_row == 0 else -1

        if curr_x == start_row:
            target_x = curr_x + (2 * direction)
            final_square = (target_x, curr_y)
            intermediate_square = (target_x - direction, curr_y)

            if (
                state.board.query_square(intermediate_square) == EMPTY_SQUARE
                and state.board.query_square(final_square) == EMPTY_SQUARE
            ):
                return Move(piece, [piece.position, final_square])

        return None

    @staticmethod
    def _get_piece_basic_moves(
        state: GameState, query_piece: Egg, piece: Egg
    ) -> list[Move | None]:
        moves = []

        curr_x, curr_y = query_piece.position

        for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            square = (curr_x + dx, curr_y + dy)
            if state.board.query_square(square) == EMPTY_SQUARE:
                moves.append(Move(piece, [piece.position, square]))

        return moves

    @staticmethod
    def _get_chain_moves(state: GameState, piece: Egg):
        moves = []

        chain = state.board.get_connected_group_chain(piece)

        if chain:
            for chain_piece in chain[1:]:
                moves += GameRules._get_piece_basic_moves(state, chain_piece, piece)

        return moves

    @staticmethod
    def get_group_mandatory_moves(state: GameState, group: int) -> list | list[Move]:
        moves = []

        for piece in state.board.get_group(group):
            moves += GameRules.get_mandatory_moves(state, piece)

        if moves:
            moves = [
                move
                for move in moves
                if len(move.captured_pieces)
                == max([len(m.captured_pieces) for m in moves])
            ]

        return moves

    @staticmethod
    def get_mandatory_moves(
        state: GameState, piece: Egg, current_move: Move = None
    ) -> list | list[Move]:
        moves = []

        if current_move is None:
            current_move = Move(piece, [piece.position])

        found_continuation = False

        for enemy in state.board.get_enemy_touching_pieces(piece):
            if landing_square := GameRules._can_i_eat(state, piece, enemy):
                found_continuation = True

                temp_move = Move(
                    piece,
                    [piece.position, landing_square],
                    [enemy],
                )
                current_move.path.append(landing_square)
                current_move.captured_pieces.append(enemy)

                state.board.apply_move(temp_move)
                moves += GameRules.get_mandatory_moves(state, piece, current_move)

                state.board.undo_move(temp_move)
                current_move.path.pop()
                current_move.captured_pieces.pop()
        if not found_continuation and len(current_move.captured_pieces) > 0:
            moves.append(deepcopy(current_move))

        return moves

    # MOVES GETTER
    # CHECKERS

    @staticmethod
    def _can_i_eat(state: GameState, piece: Egg, enemy: Egg):
        dx = enemy.position[0] - piece.position[0]
        dy = enemy.position[1] - piece.position[1]

        if abs(dx) + abs(dy) == 1:
            landing_square = (enemy.position[0] + dx, enemy.position[1] + dy)

            if state.board.query_square(landing_square) == EMPTY_SQUARE:
                return landing_square

        return ()

    @staticmethod
    def check_win(state: GameState):
        NOBODY = 0

        white_pieces = state.board.get_group(WHITE)
        black_pieces = state.board.get_group(BLACK)

        for lr_piece in [
            piece
            for piece in (white_pieces + black_pieces)
            if piece.position[0] == state.board.get_goal_row(piece.group)
        ]:
            if touching_pieces := state.board.get_enemy_touching_pieces(lr_piece):
                for enemy in touching_pieces:
                    if GameRules._can_i_eat(
                        state, lr_piece, enemy
                    ) or GameRules._can_i_eat(state, enemy, lr_piece):
                        break
                else:
                    return lr_piece.group
            else:
                return lr_piece.group

        if not black_pieces:
            return WHITE
        if not white_pieces:
            return BLACK

        if not GameRules._can_group_move(state, black_pieces):
            return WHITE
        if not GameRules._can_group_move(state, white_pieces):
            return BLACK

        return NOBODY

    @staticmethod
    def _can_group_move(state: GameState, group: int | list[Egg]):
        pieces = state.board.get_group(group) if isinstance(group, int) else group

        for piece in pieces:
            for enemy in state.board.get_enemy_touching_pieces(piece):
                if GameRules._can_i_eat(state, piece, enemy):
                    return True

        for piece in pieces:
            if (
                GameRules._get_first_square_move(state, piece)
                or GameRules._get_piece_basic_moves(state, piece, piece)
                or GameRules._get_chain_moves(state, piece)
            ):
                return True

        return False

    # CHECKERS
    # HELPERS

    @staticmethod
    def iter_legal_moves_for_group(state: GameState, group: int):
        for piece in state.board.get_group(group):
            for move in GameRules.get_piece_legal_moves(state, piece):
                yield move
