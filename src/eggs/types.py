

type Square = tuple[int, int]
OUT_OF_BOUNDS = -1
EMPTY_SQUARE = 0
WHITE = 1
BLACK = 2


type TTEDepth = int
type TTEScore = float
type TTEFlag = int
type TTEntry = tuple[TTEDepth, TTEScore, TTEFlag]
EXACT = 0
UPPER = 1
LOWER = -1

class SearchTimeOut(Exception):
    pass