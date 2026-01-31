from eggs.game_state import GameState
from eggs.board import *
from eggs.game_rules import GameRules as Rules


SIX_LINES_BOARD = [0, 0.05, 0.1, 0.25, 0.35, 1]
COLUMNS = 0.1
THREAT = 0.3

class AI:
    @staticmethod
    def minimax(state: GameState, depth: int, alpha: float, beta: float, maximizer_player: bool):
        winner = Rules.check_win(state)
        if depth == 0 or winner != 0:
            if winner == WHITE: return 100 + depth
            if winner == BLACK: return -100 - depth
            return AI.evaluate_position(state)
        
        moves = Rules.get_group_legal_moves(state, WHITE if maximizer_player else BLACK)

        if maximizer_player:
            max_eval = -float("inf")

            for move in moves:
                state.board.apply_move(move)
                eval = AI.minimax(state, depth - 1, alpha, beta, False)
                state.board.undo_move(move)

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval
        else:
            min_eval = float("inf")

            for move in moves:
                state.board.apply_move(move)
                eval = AI.minimax(state, depth - 1, alpha, beta, True)
                state.board.undo_move(move)

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval

    @staticmethod
    def choose_best_move(state: GameState, maximizer_player: bool):
        best_move = None
        depth = 4 # 4 é razoável, 5 para cima fica extremamente lento (menos quando tem poucas peças, óbvio)

        alpha, beta = -float("inf"), float("inf")
        best_score = alpha if maximizer_player else beta

        for move in Rules.get_group_legal_moves(state, WHITE if maximizer_player else BLACK):
            state.board.apply_move(move)
            score = AI.minimax(state, depth - 1, alpha, beta, not maximizer_player)
            state.board.undo_move(move)

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
    def evaluate_position(state: GameState):
        # não avalia vitória, pois o minimax já faz isso...
        board = state.board
        points = 0

        white_pieces = board.get_group(WHITE)
        black_pieces = board.get_group(BLACK)

        points += len(white_pieces) - len(black_pieces)

        for piece in (white_pieces + black_pieces):
            if piece.position[1] in [0, board.length]:
                points += 0.2 if piece.group == WHITE else -0.2
            
            if piece.group == WHITE:
                points += SIX_LINES_BOARD[piece.position[0]]
            else:
                points -= SIX_LINES_BOARD[::-1][piece.position[0]]

            for enemy in board.get_enemy_touching_pieces(piece):
                if (Rules._can_i_eat(state, piece, enemy)
                    and not Rules._can_i_eat(state, enemy, piece)):
                    points += THREAT if piece.group == WHITE else -THREAT
                if Rules._can_i_eat(state, enemy, piece):
                    points -= THREAT if piece.group == WHITE else -THREAT

        return points
