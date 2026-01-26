from eggs.board import Board
from eggs.game_state import GameState
from eggs.game_rules import GameRules

b = Board()
b.custom_board(
    [[1, 0, 0, 0, 0],
      [2, 1, 1, 0, 0],
      [1, 0, 0, 0, 0],
      [1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0 ,0 ,0 ,0 ,0]]
)
gs = GameState(b)
print(b)
print(GameRules._check_win(gs))
