from copy import deepcopy
from dataclasses import dataclass, field

@dataclass
class Pos:
    name: str
    Path: list[tuple[int, int]] 

def main():
    p1 = Pos("eric", [(0,0), (0,1)])
    
    p2 = deepcopy(p1)
    p2.Path.append((1,1))

    print(p1, p2)
if __name__ == "__main__":
    main()
