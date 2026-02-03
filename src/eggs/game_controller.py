from eggs.game_state import GameState
from eggs.game_rules import GameRules as Rules
from eggs.move import Move
from eggs.types import Square

class GameController:
    def __init__(self, state: GameState):
        self.state = state

    def make_move(self, move: Move):
        if move.group != self.state.turn:
            print("Not your turn")
            return False

        if move not in self.get_piece_legal_moves(move.start):
            return False

        self.state.board.apply_move(move)
        self.state.moves.append(move)

        if winner := Rules.check_win(self.state.board):
            self._end_game(winner)
        else:
            self.state.change_state(
                Rules.get_group_mandatory_moves(self.state.board, self.state.next_player())
            )
            # outras lógicas futuras...

        return True

    def undo_move(self):
        if not self.state.moves:
            print("Nothing to undo!")
            return

        last_move = self.state.moves.pop()
        self.state.board.undo_move(last_move)
        self.state.change_state(
            Rules.get_group_mandatory_moves(self.state.board, self.state.next_player())
        )

    # CONTROLLERS
    # GET MOVES

    def get_piece_legal_moves(self, piece_pos: Square) -> list[Move]:
        if self.state.temp_mandatory_moves:
            return [
                move for move in self.state.temp_mandatory_moves
                if move.start == piece_pos
            ]

        return Rules.get_piece_legal_moves(self.state.board, piece_pos)


    # GET MOVES

    def _end_game(self, winner: int):
        print(f"player {winner} wins")
        self.state.winner = winner
        # lógica futura...
