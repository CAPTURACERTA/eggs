from eggs.board import *
from eggs.game_state import GameState
from eggs.ai import AI
from eggs.game_rules import GameRules as Rules
from eggs.move import Move

b = Board.custom_board(
    [
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 2, 0, 0],
        [2, 2, 2, 0, 2],
    ]
)
gs = GameState(b)

print(AI.evaluate_position(b))

"""
[
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2],
]
"""