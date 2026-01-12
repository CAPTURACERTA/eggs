from dataclasses import dataclass, field
from pieces import Egg

@dataclass
class Move:
    piece: Egg
    path: list[tuple[int, int]] 
    captured_pieces: list[Egg] = field(default_factory=list)