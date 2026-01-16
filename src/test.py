from board import Board
from game_controle import GameControler
from move import Move


b = Board()
b.start()
game = GameControler(b)

p1 = b.get_group(1)
p2 = b.get_group(2)

moves = [
    Move(p1[0], [(0,0), (4,2)]), Move(p1[1], [(0,1), (1,1)])
]

i = 0
for pos in [[4,1],[3,0],[2,1],[3,2], [5,2]]:
    egg = p2[i]
    moves.append(Move(egg, [egg.position, pos]))
    i += 1
for m in moves: b.apply_move(m)

for m in game._get_group_mandatory_moves():
    print(m)
print(b)