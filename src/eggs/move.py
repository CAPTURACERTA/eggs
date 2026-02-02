from eggs.types import Square
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

    def __contains__(self, square):
        return (square in self.path or square in self.captured)