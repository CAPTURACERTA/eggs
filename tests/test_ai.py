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
ia = AI(gs, WHITE)
p1 = b.get_group(WHITE)

m = Move(p1[0], [(0,0), (0,2)])

print(p1[0] in m)
