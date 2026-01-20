from uuid import uuid4

class Egg:
    def __init__(self, group: int, position: tuple[int, int]):
        self.id = uuid4()          
        self.group = group
        self.position = position

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Egg) and self.id == other.id

    def __repr__(self):
        return "⚪" if self.group == 1 else "⚫"
