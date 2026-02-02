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
    def choose_best_move(board: Board, maximizer_player: bool):
        best_move = None
        depth = 4 # 4 é razoável, 5 para cima fica extremamente lento (menos quando tem poucas peças, óbvio)

        alpha, beta = -float("inf"), float("inf")
        best_score = alpha if maximizer_player else beta

        for move in Rules.get_group_legal_moves(board, WHITE if maximizer_player else BLACK):
            board.apply_move(move)
            score = AI.minimax(board, depth - 1, alpha, beta, not maximizer_player)
            board.undo_move(move)

            print(f"Move: {move} | Score: {score}") # debug

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

        return best_move
        
    
    @ staticmethod
    def evaluate_position(board: Board):
        # ainda estou trabalhando nisso...
        points = 0

        white_pieces = list(board.get_group_pieces(WHITE))
        black_pieces = list(board.get_group_pieces(BLACK))

        points += len(white_pieces) - len(black_pieces)

        for piece in (white_pieces + black_pieces):
            x, y = piece

            if board[piece] == WHITE:
                points += WHITE_56_BOARD[x][y]
            else:
                points -= BLACK_56_BOARD[x][y]

            if not board.is_chained(piece):
                points -= UNCHAINED if board[piece] == WHITE else -UNCHAINED

            for enemy in board.get_touching_enemies(piece):
                if (Rules._can_i_eat(board, piece, enemy)
                    and not Rules._can_i_eat(board, enemy, piece)):
                    points += THREAT if board[piece] == WHITE else -THREAT
                if Rules._can_i_eat(board, enemy, piece):
                    points -= THREAT if board[piece] == WHITE else -THREAT

        return points
