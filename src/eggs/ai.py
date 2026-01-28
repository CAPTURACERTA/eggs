from eggs.game_state import GameState
from eggs.board import *
from eggs.game_rules import GameRules as Rules

class AI:
    def __init__(self, state: GameState, group: int):
        self.state = state
        self.group = group

    def chose_move(self) -> Move:
        moves = Rules.get_group_legal_moves(self.state, self.group)
        move_points = []

        for move in moves:
            self.state.board.apply_move(move)
            move_points.append(self.evaluate_position())
            self.state.board.undo_move(move)

        return moves[move_points.index(max(move_points))]

    def evaluate_position(self):
        state = self.state
        points = 0

        win = Rules.check_win(state)
        if win and win == self.group:
            return 100
        elif win and win != self.group:
            return -100
        
        pieces = state.board.get_group(self.group)
        points_per_square = [round(n * 0.1, 2) for n in range(state.board.height)]
        if self.group == BLACK:
            points_per_square = points_per_square[::-1]

        for piece in pieces:
            points += points_per_square[piece.position[0]]
            for enemy in state.board.get_enemy_touching_pieces(piece):
                if (Rules._can_i_eat(state, piece, enemy)
                    and not Rules._can_i_eat(state, enemy, piece)):
                    points += 1
                if Rules._can_i_eat(state, enemy, piece):
                    points -= 1

        return points