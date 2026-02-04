from eggs.types import Square, WHITE, BLACK
from dataclasses import dataclass, field


@dataclass
class Move:
    group: int
    path: list[Square]
    captured: list[Square] = field(default_factory=list)

    @property
    def start(self) -> Square:
        return self.path[0] if self.path else None

    @property
    def end(self) -> Square:
        return self.path[-1] if self.path else None

    @property
    def is_forward(self):
        return self.end[0] > self.start[0] if self.group == WHITE else self.end[0] < self.start[0]

    def __contains__(self, square):
        return (square in self.path or square in self.captured)