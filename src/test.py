from board import Board
from game_controle import GameControler
from move import Move


b = Board()
b.start()
game = GameControler(b)

p1 = b.get_group(1)
p2 = b.get_group(2)


print(b)
i = 0
for egg in p1:
    i += len(game.get_legal_moves(egg))

print(i)