from eggs.board import Board
from eggs.types import *
from eggs.game_rules import GameRules as Rules
from eggs.points import *
import time



class AI:
    transposition_table: dict[tuple, TTEntry] = {}

    @staticmethod
    def minimax(
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizer_player: bool,
        end_time: float = None
    ):
        if end_time is not None and time.time() >= end_time:
            raise SearchTimeOut()

        original_alpha = alpha
        original_beta = beta 
        
        state_key = (board.to_tuple(), maximizer_player)
        if state_key in AI.transposition_table:
            entry = AI.transposition_table[state_key]
            tt_depth, tt_score, tt_flag = entry
            if tt_depth >= depth:
                if tt_flag == EXACT: return tt_score
                elif tt_flag == LOWER: alpha = max(alpha, tt_score)
                elif tt_flag == UPPER: beta = min(beta, tt_score)
                if alpha >= beta: return tt_score

        winner = Rules.check_win(board)
        if depth == 0 or winner != 0:
            if winner == WHITE: return 100 + depth
            if winner == BLACK: return -100 - depth
            return AI.evaluate_position(board)
        
        moves = Rules.get_group_legal_moves(board, WHITE if maximizer_player else BLACK)
        moves.sort(key=lambda m: m.is_forward, reverse=True)

        best_score = -float("inf") if maximizer_player else float("inf")
        
        for move in moves:
            board.apply_move(move)
            
            try:
                val = AI.minimax(board, depth - 1, alpha, beta, not maximizer_player, end_time)
                
                if maximizer_player:
                    best_score = max(best_score, val)
                    alpha = max(alpha, val)
                else:
                    best_score = min(best_score, val)
                    beta = min(beta, val)
                    
            finally:
                board.undo_move(move)

            if beta <= alpha:
                break 

        entry_flag = EXACT
        if best_score <= original_alpha:
            entry_flag = UPPER
        elif best_score >= original_beta:
            entry_flag = LOWER
        
        AI.transposition_table[state_key] = (depth, best_score, entry_flag)

        return best_score
        
    @staticmethod
    def choose_best_move(board: Board, maximizer_player: bool, time_limit: float):
        start_time = time.time()
        end_time = start_time + time_limit
        
        best_move_global = None
        best_score_global = -float("inf") if maximizer_player else float("inf")
        
        current_depth = 1
        
        try:
            while True:
                if time.time() >= end_time:
                    break

                print(f"--- Iniciando Profundidade {current_depth} ---")
                
                current_best_move = None
                alpha, beta = -float("inf"), float("inf")
                
                moves = Rules.get_group_legal_moves(board, WHITE if maximizer_player else BLACK)
                moves.sort(key=lambda m: m.is_forward, reverse=True)

                iteration_best_score = -float("inf") if maximizer_player else float("inf")

                for move in moves:
                    board.apply_move(move)
                    try:
                        score = AI.minimax(
                            board, current_depth - 1, alpha, beta, not maximizer_player, end_time
                        )
                    except SearchTimeOut:
                        board.undo_move(move)
                        raise SearchTimeOut()
                    
                    board.undo_move(move)

                    if maximizer_player:
                        if score > iteration_best_score:
                            iteration_best_score = score
                            current_best_move = move
                        alpha = max(alpha, score)
                    else:
                        if score < iteration_best_score:
                            iteration_best_score = score
                            current_best_move = move
                        beta = min(beta, score)

                best_move_global = current_best_move
                best_score_global = iteration_best_score
                
                print(f"Profundidade {current_depth} concluída. Melhor: {best_move_global} Score: {best_score_global}")
                
                if abs(best_score_global) > 50: 
                    print("Vitória encontrada, parando busca.")
                    break

                current_depth += 1

        except SearchTimeOut:
            print(f"Tempo esgotado! Retornando melhor movimento da profundidade {current_depth - 1}")
        
        return best_move_global

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