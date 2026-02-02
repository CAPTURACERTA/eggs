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
        
        for piece in pieces:
            moves += GameRules.get_piece_legal_moves(board, piece)

        return moves

    @staticmethod
    def get_piece_legal_moves(board: Board, piece: Square):
        moves = []

        if move := GameRules._get_first_square_move(board, piece):
            moves.append(move)
        moves += GameRules._get_piece_basic_moves(board, piece, piece)
        moves += GameRules._get_chain_moves(board, piece)

        return moves

    @staticmethod
    def _get_first_square_move(board: Board, piece: Square):
        curr_x, curr_y = piece

        start_row = board.get_start_row(board[piece])
        direction = 1 if start_row == 0 else -1

        if curr_x == start_row:
            target_x = curr_x + (2 * direction)
            final_square = (target_x, curr_y)
            intermediate_square = (target_x - direction, curr_y)

            if (
                board.query_square(intermediate_square) == EMPTY_SQUARE
                and board.query_square(final_square) == EMPTY_SQUARE
            ):
                return Move(board[piece], [piece, final_square])

        return None

    @staticmethod
    def _get_piece_basic_moves(
        board: Board, query_piece: Square, piece: Square
    ) -> list[Move | None]:
        moves = []

        curr_x, curr_y = query_piece

        for dx, dy in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            square = (curr_x + dx, curr_y + dy)
            if board.query_square(square) == EMPTY_SQUARE:
                moves.append(Move(board[piece], [piece, square]))

        return moves

    @staticmethod
    def _get_chain_moves(board: Board, piece: Square):
        moves = []

        chain = board.get_connected_group_chain(piece)

        if chain:
            for chain_piece in chain[1:]:
                moves += GameRules._get_piece_basic_moves(board, chain_piece, piece)

        return moves

    @staticmethod
    def get_group_mandatory_moves(board: Board, group: int) -> list | list[Move]:
        pieces = board.get_group_pieces(group)
        moves = []

        for piece in list(pieces):
            moves += GameRules.get_mandatory_moves(board, piece)

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
        board: Board, piece: Square, current_move: Move = None
    ) -> list | list[Move]:
        moves = []

        if current_move is None:
            current_move = Move(board[piece], [piece])

        found_continuation = False

        for enemy in board.get_touching_enemies(piece):
            if landing_square := GameRules._can_i_eat(board, piece, enemy):
                found_continuation = True

                temp_move = Move(
                    board[piece],
                    [piece, landing_square],
                    [enemy],
                )
                current_move.path.append(landing_square)
                current_move.captured.append(enemy)

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
    def _can_i_eat(board: Board, piece: Square, enemy: Square):
        dx = enemy[0] - piece[0]
        dy = enemy[1] - piece[1]

        if abs(dx) + abs(dy) == 1:
            landing_square = (enemy[0] + dx, enemy[1] + dy)

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
