from board import Board
from game_controle import GameControler
from move import Move


b = Board()
b.start()
game = GameControler(b)

p1 = b.get_group(1)
p2 = b.get_group(2)

b.apply_move(
    Move(
        p1[0],
        [(0,0), (2,0)],
        [p2[0],]
    )
)

print(b)