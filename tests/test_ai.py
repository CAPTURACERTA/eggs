from eggs.board import *
from eggs.game_state import GameState
from eggs.ai import AI
from eggs.game_rules import GameRules as Rules
from eggs.move import Move

b = Board.custom_board(
    [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 2, 2, 0],
    ]
)
gs = GameState(b)

print(b)
# print(
#     f"white: {AI.evaluate_position(gs, WHITE)}\nblack: {AI.evaluate_position(gs, BLACK)}"
# )
b.apply_move(AI.choose_best_move(gs, False))
print(b)
