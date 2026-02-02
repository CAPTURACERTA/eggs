from eggs.board import *
from eggs.game_state import GameState
from eggs.ai import AI
from eggs.game_rules import GameRules as Rules
from eggs.move import Move

b = Board.custom_board(
    [
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2],
    ]
)
gs = GameState(b)

print(b)
p1 = b.get_group_pieces(WHITE)
print(p1)
b.apply_move(
    Move(WHITE, [(0,0),(2,0)])
)
print(b)
print(p1)

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