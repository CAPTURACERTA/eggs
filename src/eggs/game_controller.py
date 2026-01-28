from eggs.game_state import GameState
from eggs.game_rules import GameRules as Rules
from eggs.move import Move
from eggs.pieces import Egg


class GameController:
    def __init__(self, state: GameState):
        self.state = state

    def make_move(self, move: Move):
        if move.piece.group != self.state.turn:
            print("Not your turn")
            return False

        if move not in self.get_piece_legal_moves(move.piece):
            return False

        self.state.board.apply_move(move)
        self.state.moves.append(move)

        if winner := Rules.check_win(self.state):
            self._end_game(winner)
        else:
            self.state.change_state(
                Rules.get_group_mandatory_moves(self.state, self.state.next_player())
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
            Rules.get_group_mandatory_moves(self.state, self.state.next_player())
        )

    # CONTROLLERS
    # GET MOVES

    def get_piece_legal_moves(self, piece: Egg):
        moves = []

        if self.state.temp_mandatory_moves:
            return [
                move for move in self.state.temp_mandatory_moves if move.piece == piece
            ]

        if piece in self.state.temp_pieces_moves:
            return self.state.temp_pieces_moves[piece]

        if moves := Rules.get_piece_legal_moves(self.state, piece):
            self.state.temp_pieces_moves[piece] = moves

        return moves

    # GET MOVES

    def _end_game(self, winner: int):
        print(f"player {winner} wins")
        self.state.winner = winner
        # lógica futura...
