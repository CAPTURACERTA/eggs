from eggs.board import *
from eggs.game_rules import GameRules as Rules
from eggs.points import *



class AI:
    @staticmethod
    def minimax(board: Board, depth: int, alpha: float, beta: float, maximizer_player: bool):
        winner = Rules.check_win(board)
        if depth == 0 or winner != 0:
            if winner == WHITE: return 100 + depth
            if winner == BLACK: return -100 - depth
            return AI.evaluate_position(board)
        
        moves = Rules.get_group_legal_moves(board, WHITE if maximizer_player else BLACK)
        moves.sort(key= lambda m: m.is_forward, reverse=True)

        if maximizer_player:
            max_eval = -float("inf")

            for move in moves:
                board.apply_move(move)
                eval = AI.minimax(board, depth - 1, alpha, beta, False)
                board.undo_move(move)

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval
        else:
            min_eval = float("inf")

            for move in moves:
                board.apply_move(move)
                eval = AI.minimax(board, depth - 1, alpha, beta, True)
                board.undo_move(move)

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval

    @staticmethod
    def choose_best_move(board: Board, depth: int, maximizer_player: bool):
        best_move = None

        alpha, beta = -float("inf"), float("inf")
        best_score = alpha if maximizer_player else beta

        moves = Rules.get_group_legal_moves(board, WHITE if maximizer_player else BLACK)
        moves.sort(key= lambda m: m.is_forward, reverse=True)

        for move in moves:
            board.apply_move(move)
            score = AI.minimax(board, depth - 1, alpha, beta, not maximizer_player)
            board.undo_move(move)

            print(f"Move: {move} | Score: {score}") 

            if maximizer_player:
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)

        print(f"Chosen: {best_move} | Score: {best_score}")
        return best_move
        
    
    @ staticmethod
    def evaluate_position(board: Board):
        white_score, black_score = 0, 0

        white_pieces = list(board.get_group_pieces(WHITE))
        white_score += len(white_pieces) 

        for piece_pos in white_pieces:
            x, y = piece_pos

            white_score += WHITE_56_BOARD[x][y]
            if not board.is_chained(piece_pos):
                white_score -= UNCHAINED 

            for enemy_pos in board.get_touching_enemies(piece_pos):
                if not Rules._can_i_eat(board, enemy_pos, piece_pos):
                    white_score += THREAT


        black_pieces = list(board.get_group_pieces(BLACK))
        black_score += len(black_pieces)

        for piece_pos in black_pieces:
            x, y = piece_pos

            black_score += BLACK_56_BOARD[x][y]

            if not board.is_chained(piece_pos):
                black_score -= UNCHAINED

            for enemy_pos in board.get_touching_enemies(piece_pos):
                if not Rules._can_i_eat(board, enemy_pos, piece_pos):
                    black_score += THREAT

        final_score = white_score - black_score

        return final_score if not (abs(final_score) < 1e-9) else 0