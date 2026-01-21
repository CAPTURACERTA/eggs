from eggs.board import Board
from eggs.game_controller import GameController

b = Board()
b.start()
game = GameController(b)

p1 = b.get_group(1)
p2 = b.get_group(2)

turn = 1

while True:
    print(b)

    piece = None
    while not isinstance(piece, int):
        try:
            piece = int(input("> piece: ").strip())
        except Exception as e:
            continue

    print("> legal moves:")
    i = 0
    moves = game.get_legal_moves(p1[piece] if turn == 1 else p2[piece])
    for move in moves:
        print(f"> {i} - {move}")
        i += 1
    
    try:
        move = int(input("> move: ").strip())
        game.make_move(moves[move])
        turn = 2 if turn == 1 else 1
    except Exception as e:
        continue
