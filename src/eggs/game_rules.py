from eggs.board import Board
from eggs.move import Move
from eggs.types import *


class GameRules:
    # MOVES GETTERS

    @staticmethod
    def get_group_legal_moves(board: Board, group: int):
        moves = []
        pieces = board.get_group_pieces(group)

        moves += GameRules.get_group_mandatory_moves(board, group)
        if moves:
            return moves
        
        for piece_pos in pieces:
            moves += GameRules.get_piece_legal_moves(board, piece_pos)

        return moves

    @staticmethod
    def get_piece_legal_moves(board: Board, piece_pos: Square):
        moves = []

        if move := GameRules._get_first_square_move(board, piece_pos):
            moves.append(move)
        moves += GameRules._get_piece_basic_moves(board, piece_pos, piece_pos)
        moves += GameRules._get_chain_moves(board, piece_pos)

        return moves

    @staticmethod
    def _get_first_square_move(board: Board, piece_pos: Square):
        curr_x, curr_y = piece_pos

        start_row = board.get_start_row(board[piece_pos])
        direction = 1 if start_row == 0 else -1

        if curr_x == start_row:
            target_x = curr_x + (2 * direction)
            final_square = (target_x, curr_y)
            intermediate_square = (target_x - direction, curr_y)

            if (
                board.query_square(intermediate_square) == EMPTY_SQUARE
                and board.query_square(final_square) == EMPTY_SQUARE
            ):
                return Move(board[piece_pos], [piece_pos, final_square])

        return None

    @staticmethod
    def _get_piece_basic_moves(
        board: Board, ref_piece_pos: Square, piece_pos: Square
    ) -> list[Move | None]:
        moves = []

        curr_x, curr_y = ref_piece_pos

        for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            square = (curr_x + dx, curr_y + dy)
            if board.query_square(square) == EMPTY_SQUARE:
                moves.append(Move(board[piece_pos], [piece_pos, square]))

        return moves

    @staticmethod
    def _get_chain_moves(board: Board, piece_pos: Square):
        moves = []

        chain = board.get_connected_group_chain(piece_pos)

        if chain:
            for chained_pos in chain[1:]:
                moves += GameRules._get_piece_basic_moves(board, chained_pos, piece_pos)

        return moves

    @staticmethod
    def get_group_mandatory_moves(board: Board, group: int) -> list | list[Move]:
        pieces = list(board.get_group_pieces(group))
        moves = []

        for piece_pos in pieces:
            moves += GameRules.get_mandatory_moves(board, piece_pos)

        if moves:
            moves = [
                move
                for move in moves
                if len(move.captured)
                == max([len(m.captured) for m in moves])
            ]

        return moves

    @staticmethod
    def get_mandatory_moves(
        board: Board, piece_pos: Square, current_move: Move = None
    ) -> list | list[Move]:
        moves = []

        if current_move is None:
            current_move = Move(board[piece_pos], [piece_pos])

        found_continuation = False

        for enemy_pos in board.get_touching_enemies(piece_pos):
            if landing_square := GameRules._can_i_eat(board, piece_pos, enemy_pos):
                found_continuation = True

                temp_move = Move(
                    board[piece_pos],
                    [piece_pos, landing_square],
                    [enemy_pos],
                )
                current_move.path.append(landing_square)
                current_move.captured.append(enemy_pos)

                board.apply_move(temp_move)
                moves += GameRules.get_mandatory_moves(board, landing_square, current_move)

                board.undo_move(temp_move)
                current_move.path.pop()
                current_move.captured.pop()

        if not found_continuation and len(current_move.captured) > 0:
            moves.append(
                Move(
                    current_move.group,
                    list(current_move.path),
                    list(current_move.captured)
                )
            )

        return moves

    # MOVES GETTER
    # CHECKERS

    @staticmethod
    def _can_i_eat(board: Board, piece_pos: Square, enemy_pos: Square) -> Square | tuple[()]:
        dx = enemy_pos[0] - piece_pos[0]
        dy = enemy_pos[1] - piece_pos[1]

        if abs(dx) + abs(dy) == 1:
            landing_square = (enemy_pos[0] + dx, enemy_pos[1] + dy)

            if board.query_square(landing_square) == EMPTY_SQUARE:
                return landing_square

        return ()

    @staticmethod
    def check_win(board: Board):
        NOBODY = 0

        white_pieces = board.get_group_pieces(WHITE)
        black_pieces = board.get_group_pieces(BLACK)
        all_pieces = [*white_pieces, *black_pieces]

        if lr_pieces := [
            piece
            for piece in all_pieces
            if piece[0] == board.get_goal_row(board[piece])
        ]:
            all_mandatory_moves = [
                move 
                for piece in all_pieces 
                for move in GameRules.get_mandatory_moves(board, piece)
            ]
            
            for lr_piece in lr_pieces:
                for move in all_mandatory_moves:
                    if lr_piece in move:
                        break
                else:
                    return board[lr_piece]

        if not black_pieces:
            return WHITE
        if not white_pieces:
            return BLACK

        if not GameRules._can_group_move(board, BLACK):
            return WHITE
        if not GameRules._can_group_move(board, WHITE):
            return BLACK

        return NOBODY

    @staticmethod
    def _can_group_move(board: Board, group: int):
        pieces = board.get_group_pieces(group)

        for piece in pieces:
            for enemy in board.get_touching_enemies(piece):
                if GameRules._can_i_eat(board, piece, enemy):
                    return True

        for piece in pieces:
            if (
                GameRules._get_first_square_move(board, piece)
                or GameRules._get_piece_basic_moves(board, piece, piece)
                or GameRules._get_chain_moves(board, piece)
            ):
                return True

        return False

    # CHECKERS
