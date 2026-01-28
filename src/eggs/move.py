from dataclasses import dataclass, field
from eggs.pieces import Egg


@dataclass
class Move:
    piece: Egg
    path: list[tuple[int, int]]
    captured_pieces: list[Egg] = field(default_factory=list)

    def __contains__(self, item):
        # checks for eggs, but could check for paths as well
        return (item == self.piece or item in self.captured_pieces)